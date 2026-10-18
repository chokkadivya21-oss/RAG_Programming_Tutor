"""
Code Visualization & Execution Tracer Module
Provides step-by-step code tracking, variable state diffing, standard output capture,
educational natural-language explanations, and flowchart generation.
"""

import ast
import io
import sys
import copy
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class ExecutionStep:
    step_num: int
    line_no: int
    code_text: str
    event: str
    variables: Dict[str, Any]
    variable_types: Dict[str, str]
    changed_vars: Dict[str, Any]
    stdout_step: str
    cumulative_stdout: str
    explanation: str


class StepExecutionTracer:
    def __init__(self, max_steps: int = 150):
        self.max_steps = max_steps
        self.steps: List[ExecutionStep] = []
        self.source_lines: List[str] = []
        self.step_counter = 0
        self.prev_locals: Dict[str, Any] = {}
        self.captured_output = io.StringIO()
        self.last_stdout_pos = 0

    def trace_code(self, code_str: str) -> Dict[str, Any]:
        """
        Executes code line by line with tracing hook, capturing variable states
        and output.
        """
        self.steps = []
        self.source_lines = code_str.splitlines()
        self.step_counter = 0
        self.prev_locals = {}
        self.captured_output = io.StringIO()
        self.last_stdout_pos = 0

        # Validate syntax and compile to code object
        try:
            compiled = compile(code_str, "<student_code>", "exec")
        except SyntaxError as e:
            return {
                "success": False,
                "error": f"Syntax Error on line {e.lineno}: {e.msg}",
                "steps": [],
                "source_lines": self.source_lines,
                "total_output": "",
            }

        # Safe execution namespace
        safe_builtins = {
            "print": self._custom_print,
            "range": range,
            "len": len,
            "sum": sum,
            "min": min,
            "max": max,
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
            "round": round,
            "abs": abs,
            "enumerate": enumerate,
            "zip": zip,
            "sorted": sorted,
            "reversed": reversed,
        }
        safe_globals = {"__builtins__": safe_builtins}
        safe_locals = {}

        old_trace = sys.gettrace()
        old_stdout = sys.stdout

        try:
            sys.settrace(self._trace_hook)
            exec(compiled, safe_globals, safe_locals)
        except Exception as e:
            self._record_error_step(str(e))
        finally:
            sys.settrace(old_trace)
            sys.stdout = old_stdout

        # If any lingering uncaptured stdout remains
        final_out = self.captured_output.getvalue()
        if self.steps and self.last_stdout_pos < len(final_out):
            diff = final_out[self.last_stdout_pos:]
            self.steps[-1].stdout_step += diff
            self.steps[-1].cumulative_stdout = final_out
            self.last_stdout_pos = len(final_out)

        # Add explicit clean loop/program termination step
        if self.steps:
            last = self.steps[-1]
            self.steps.append(ExecutionStep(
                step_num=len(self.steps) + 1,
                line_no=last.line_no,
                code_text="# Program Finished",
                event="end",
                variables=last.variables,
                variable_types=last.variable_types,
                changed_vars={},
                stdout_step="",
                cumulative_stdout=final_out,
                explanation="Execution complete. The program has finished running and all statements completed.",
            ))

        return {
            "success": True,
            "error": None,
            "steps": self.steps,
            "source_lines": self.source_lines,
            "total_output": self.captured_output.getvalue(),
        }

    def _custom_print(self, *args, **kwargs):
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        text = sep.join(str(a) for a in args) + end
        self.captured_output.write(text)

    def _trace_hook(self, frame, event, arg):
        if self.step_counter >= self.max_steps:
            return self._trace_hook

        code_obj = frame.f_code
        if code_obj.co_filename not in ("<student_code>", "<string>"):
            return self._trace_hook

        if event not in ("line", "return"):
            return self._trace_hook

        line_no = frame.f_lineno
        if line_no < 1 or line_no > len(self.source_lines):
            return self._trace_hook

        code_text = self.source_lines[line_no - 1].strip()
        if not code_text or code_text.startswith("#"):
            return self._trace_hook

        # Capture newly printed text during previous/this step
        all_output = self.captured_output.getvalue()
        stdout_step = all_output[self.last_stdout_pos:]
        self.last_stdout_pos = len(all_output)

        # Attach previous stdout to previous step if it just emitted
        if stdout_step and self.steps:
            if not self.steps[-1].stdout_step:
                self.steps[-1].stdout_step = stdout_step.strip()
                self.steps[-1].cumulative_stdout = all_output

        # Snapshot local variables (sanitize for safety)
        current_locals = {}
        var_types = {}
        for k, v in frame.f_locals.items():
            if not k.startswith("__"):
                try:
                    current_locals[k] = copy.deepcopy(v)
                except Exception:
                    current_locals[k] = str(v)
                var_types[k] = type(v).__name__

        # Compute variable changes
        changed_vars = {}
        for k, v in current_locals.items():
            if k not in self.prev_locals or self.prev_locals[k] != v:
                changed_vars[k] = v

        # Build educational explanation
        explanation = self._generate_explanation(line_no, code_text, changed_vars, current_locals)

        self.step_counter += 1
        step = ExecutionStep(
            step_num=self.step_counter,
            line_no=line_no,
            code_text=code_text,
            event=event,
            variables=copy.deepcopy(current_locals),
            variable_types=var_types,
            changed_vars=changed_vars,
            stdout_step="",
            cumulative_stdout=all_output,
            explanation=explanation,
        )
        self.steps.append(step)
        self.prev_locals = copy.deepcopy(current_locals)

        return self._trace_hook

    def _generate_explanation(
        self,
        line_no: int,
        code_text: str,
        changed_vars: Dict[str, Any],
        current_locals: Dict[str, Any],
    ) -> str:
        """Constructs human-friendly pedagogic explanation for each execution step."""
        # Case 1: For loop header
        if code_text.startswith("for "):
            if changed_vars:
                var_str = ", ".join(f"`{k} = {repr(v)}`" for k, v in changed_vars.items())
                return f"Loop iteration starting. Next value assigned: {var_str}. Condition satisfied, proceeding into loop body."
            return f"Checking loop condition: iterating through sequence items."

        # Case 2: While loop header
        if code_text.startswith("while "):
            return f"Checking `while` condition. Evaluates to True, continuing iteration."

        # Case 3: Print statement
        if "print(" in code_text:
            var_preview = [f"`{k}={repr(v)}`" for k, v in current_locals.items()]
            vars_ctx = f" (Current state: {', '.join(var_preview)})" if var_preview else ""
            return f"Executing `{code_text}`. Formats and writes text to standard output{vars_ctx}."

        # Case 4: Branching If/Elif
        if code_text.startswith(("if ", "elif ")):
            return f"Evaluating conditional statement `{code_text}`. Condition branch selected."

        # Case 5: Variable Assignment
        if "=" in code_text:
            if changed_vars:
                var_str = ", ".join(f"`{k} = {repr(v)}`" for k, v in changed_vars.items())
                return f"Assignment evaluated. Updated variable state: {var_str}."
            return f"Executed assignment: `{code_text}`."

        # Case 6: Method call (append, pop, etc.)
        if any(method in code_text for method in [".append(", ".pop(", ".insert(", ".update("]):
            return f"Data structure mutated via method `{code_text}`."

        return f"Executing line {line_no}: `{code_text}`."

    def _record_error_step(self, err_msg: str):
        self.steps.append(ExecutionStep(
            step_num=len(self.steps) + 1,
            line_no=len(self.source_lines),
            code_text="# Runtime Exception Occurred",
            event="error",
            variables=self.prev_locals,
            variable_types={},
            changed_vars={},
            stdout_step="",
            cumulative_stdout=self.captured_output.getvalue(),
            explanation=f"Runtime Error: {err_msg}",
        ))


def generate_flowchart_mermaid(code_str: str, current_line: int = -1) -> str:
    """
    Parses code into AST and generates a Mermaid flowchart highlighting active line.
    """
    try:
        ast.parse(code_str)
    except Exception:
        return ""

    nodes = ["flowchart TD", "    Start([🚀 Start]) --> N1"]
    lines = code_str.splitlines()

    for idx, line in enumerate(lines, start=1):
        clean = line.strip()
        if not clean or clean.startswith("#"):
            continue

        label = clean.replace('"', "'")
        is_active = (idx == current_line)

        if len(label) > 35:
            label = label[:32] + "..."

        curr = f"N{idx}"
        style_flag = ":::active" if is_active else ""

        if clean.startswith(("for ", "while ")):
            nodes.append(f'    {curr}{{"🔄 Loop: {label}"}}{style_flag}')
        elif clean.startswith(("if ", "elif ")):
            nodes.append(f'    {curr}{{"❓ Condition: {label}"}}{style_flag}')
        elif "print(" in clean:
            nodes.append(f'    {curr}[/"🖨️ {label}"/]{style_flag}')
        else:
            nodes.append(f'    {curr}["⚙️ {label}"]{style_flag}')

        if idx > 1:
            prev = f"N{idx-1}"
            nodes.append(f"    {prev} --> {curr}")

    final_node = f"N{len(lines)}"
    nodes.append(f"    {final_node} --> End([🏁 End])")
    nodes.append("    classDef active fill:#22c55e,stroke:#15803d,stroke-width:3px,color:#ffffff,font-weight:bold;")

    return "\n".join(nodes)
