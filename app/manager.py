from agents import Runner
from typing import List, Dict, Any
import json

from app.agents.planner import planner_agent
from app.agents.executor import executor_agent
from app.agents.evaluator import evaluator_agent
from app.types.context import ExecutorContext
from app.types.output import TaskItem, UserQueryPlan, EvaluatorResult
from app.utils.logging import setup_logger


class Manager:
    """Class that manages AI agent workflow, coordinating the plan-execute-evaluate cycle"""

    def __init__(self):
        """Initialize manager and set up logging"""
        self.logger = setup_logger(name="manager")

    async def run(self, query: str) -> str:
        """
        Execute the complete AI agent workflow

        Args:
            query: User input question

        Returns:
            str: Task completion result
        """
        self.logger.info(f"Starting to process user query: {query}")

        # 1. Generate plan using planner agent
        self.logger.info("Calling planner agent to generate execution plan")
        plan_result = await Runner.run(planner_agent, input=query)
        plan: UserQueryPlan = plan_result.final_output_as(UserQueryPlan)
        self.logger.info(
            f"Generated execution plan: {json.dumps([t.model_dump() for t in plan.tasks], ensure_ascii=False)}")

        # Extract tasks from plan
        tasks = plan.tasks
        if not tasks:
            self.logger.warning(
                "Unable to generate a valid execution plan for the user query")
            return "Unable to generate a valid execution plan for your question."

        # 2. Create execution context
        self.logger.info(
            f"Creating execution context, number of tasks: {len(tasks)}")
        context = ExecutorContext(
            goal=query,
            tasks=tasks,
            finished=False,
            current_task=tasks[0],
            execution_history=[]
        )

        results = []
        task_index = 0

        # 3. Execute plan-execute-evaluate loop until all tasks are completed
        self.logger.info("Starting plan-execute-evaluate loop")
        while not context.finished and task_index < len(tasks):
            # Update current task
            context.current_task = tasks[task_index]
            self.logger.info(
                f"Executing task {task_index + 1}/{len(tasks)}: {context.current_task.task}")

            # Execute current task
            self.logger.info("Calling executor agent")
            if task_index == 0:
                # first task
                executor_result = await Runner.run(executor_agent, input=context.current_task.task, context=context)
            else:
                # not first task
                execution_history_text = "\n".join(context.execution_history)
                executor_result = await Runner.run(executor_agent, input=f"{context.current_task.task}\nExecution History:\n{execution_history_text}", context=context)
                self.logger.debug(
                    f"Executor agent input list: {executor_result.to_input_list()}")
                
            self.logger.debug(
                f"Executor agent result: {executor_result.final_output}")

            # Record execution history
            execution_result = f"Task {task_index + 1}: {context.current_task.task}\nExecution Result: {executor_result.final_output}"
            context.execution_history.append(execution_result)

            # Evaluate execution result
            self.logger.info("Calling evaluator agent")
            evaluator_result = await Runner.run(evaluator_agent, input=f"last_task: {context.current_task}, execution_result: {execution_result}, please evaluate the result.", context=context)
            eval_output: EvaluatorResult = evaluator_result.final_output_as(
                EvaluatorResult)
            self.logger.info(
                f"Evaluation status: {eval_output.status}, next action: {eval_output.action}")

            # Determine next action based on evaluation result
            if eval_output.status == "completed":
                # Task completed, save result and continue to next task
                self.logger.info(f"Task {task_index + 1} completed")
                results.append(
                    f"Task {task_index + 1} completed: {context.current_task.task}")
                task_index += 1
            elif eval_output.action == "continue_execution_plan":
                # Continue with the next task
                self.logger.info(
                    f"Task {task_index + 1} completed, continuing execution plan")
                results.append(
                    f"Task {task_index + 1} completed: {context.current_task.task}")
                task_index += 1
            elif eval_output.action == "retry_current_task":
                # Need to retry current task, don't increment index
                self.logger.warning(f"Need to retry task {task_index + 1}")
                context.execution_history.append(
                    f"Evaluation Result: Need to retry task {task_index + 1}")
            elif eval_output.action == "adjust_task_plan":
                # Need to replan, call planner again
                self.logger.warning("Need to adjust execution plan")
                context.execution_history.append(
                    f"Evaluation Result: Need to adjust plan")
                self.logger.info("Recalling planner agent")
                new_plan_result = await Runner.run(planner_agent, f"{query}\nAdjust plan based on execution history: {context.execution_history}")
                new_plan: UserQueryPlan = new_plan_result.final_output_as(
                    UserQueryPlan)
                self.logger.info(
                    f"Adjusted execution plan: {json.dumps([t.model_dump() for t in new_plan.tasks], ensure_ascii=False)}")

                # Update task list
                tasks = new_plan.tasks
                context.tasks = tasks

                # If no tasks, end loop
                if not tasks:
                    self.logger.warning(
                        "Adjusted plan contains no tasks, terminating execution")
                    context.finished = True
                    break

                # Reset task index
                task_index = 0
            elif eval_output.action == "terminate_execution":
                # Terminate execution
                self.logger.warning(
                    f"Terminating execution: {eval_output.summary}")
                context.finished = True
                results.append(f"Execution terminated: {eval_output.summary}")
                break

            # Check if all tasks are completed
            if task_index >= len(tasks):
                self.logger.info("All tasks completed")
                context.finished = True

        # 4. Return execution results
        if context.finished:
            final_result = "\n".join(results) + "\n\nFinal Result: " + \
                context.execution_history[-1].split("Execution Result: ")[-1]
            self.logger.info("Execution completed, returning results")
            self.logger.debug(f"Final result: {final_result}")
            return final_result
        else:
            partial_result = "Tasks could not be fully completed. Current progress:\n" + \
                "\n".join(results)
            self.logger.warning("Tasks could not be fully completed")
            self.logger.debug(f"Partial result: {partial_result}")
            return partial_result
