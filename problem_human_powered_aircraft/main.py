import json
import logging
from os import path
from traceback import format_exc
from typing import Any, Mapping

import click
import yaml
from jsonschema import validate

import pickle
import os

LOGGER = logging.getLogger(__name__)


def load_config(ctx, _, value) -> dict:
    """Load `ctx.default_map` from a file.
    Parameters
    ----------
    ctx :
        Click context

    _ :

    value :
        File name

    Returns
    -------
    dict :
        Loaded config
    """
    if not path.exists(value):
        return {}
    with open(value, encoding="utf-8") as file:
        ctx.default_map = yaml.safe_load(file)
        if not isinstance(ctx.default_map, dict):
            raise TypeError(f"The content of `{value}` must be dict, but {type(ctx.default_map)}.")
    return ctx.default_map


def load_function(problem: str):
    """Load class object defining objective functions and constraints

    Parameters
    ----------
    problem : str
        problem ID
        e.g., 'hpa201-1'

    Returns
    -------
    object
        class object defining objective functions and constraints
    """
    with open(os.path.join("problem_human_powered_aircraft", "function" , problem+".pickle"), mode="rb") as file:
        func = pickle.load(file)
    return func


def define_schema(func):
    type_var = "array"
    len_min_var = func.nx
    len_max_var = func.nx
    type_var_item = "number"
    val_min_var = 0.0
    val_max_var = 1.0
    INPUT_JSONSCHEMA = {
        "$schema": "https://json-schema.org/draft/2020-12",
        "title": "input schema",
        "type": "object",
        "properties": {
            "variable": {
                "type": type_var,
                "minItems": len_min_var,
                "maxItems": len_max_var,
                "items": {
                    "type": type_var_item,
                    "minimum": val_min_var,
                    "maximum": val_max_var
                }
            }
        }
    }

    return INPUT_JSONSCHEMA


def validate_input(input_obj, func) -> None:
    """validate input format

    Parameters
    ----------
    input_obj : dict
        Design variables
        e.g., {"variable": list[float]}

    func : object
        class defining a problem

    Returns
    -------
    """

    schema = define_schema(func)

    if not schema:
        LOGGER.warning("Empty schema. Therefore, the input will not be validated.")
        return

    if isinstance(schema, str):
        validate(input_obj, json.loads(schema))
    else:
        validate(input_obj, schema)


def calc_evaluation(input_obj: dict, func):
    """Evaluate objective functions and constraints

    Parameters
    ----------
    input_obj : dict
        Design variables
        e.g., {"variable": list[float]}

    func : object
        class defining a problem

    Returns
    -------
    list[float]
        Objective function values
    
    Union[list[float], None]
        Constraint function values or None if no constraint
    """

    try:
        x = input_obj["variable"]
        if func.ng > 0:
            f, g = func(x)
            return f.tolist(), g.tolist()
        else:
            return func(x).tolist(), None
    except:
        return None, None 


def format_output(out_obj, out_con) -> Mapping[str, Any]:
    """Format evaluation results

    Parameters
    ----------
    out_obj: list
        Objective function values or None if evaluation fails
    
    out_con: list
        Constraint function values or None if no constraint

    Returns
    -------
    Mapping
        * `objective` : list[float]
        * `constraint`: Union[list[float], None]
        * `error` : None
        * `info` : None
    """

    return {"objective": out_obj, "constraint": out_con, "error": None, "info": None}


def evaluate(input_obj, func) -> Mapping[str, Any]:
    """Evaluate and format objective functions and constraints

    Parameters
    ----------
    input_obj : dict
        Design variables
        e.g., {"variable": list[float]}

    func : object
        class defining a problem

    Returns
    -------
    Mapping
        * `objective` : list[float]
        * `constraint`: Union[list[float], None]
        * `error` : None
        * `info` : None
    """

    LOGGER.info("Calculate on input...")
    out_obj, out_con = calc_evaluation(input_obj, func)
    LOGGER.debug("out_obj = %s", out_obj)
    LOGGER.debug("out_con = %s", out_con)
    LOGGER.info("...Calculated.")

    LOGGER.info("Format output...")
    out_formatted = format_output(out_obj, out_con)
    LOGGER.debug("out_formatted = %s", out_formatted)
    LOGGER.info("...Formatted.")

    return out_formatted


@click.command()
@click.option("-q", "--quiet", count=True, help="Be quieter.")
@click.option("-v", "--verbose", count=True, help="Be more verbose.")
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False),
    default="config.yml",
    is_eager=True,
    callback=load_config,
    help="Configuration file.",
)
@click.version_option("0.0.1")
@click.pass_context
def main(ctx, quiet, verbose, config) -> None:  # pylint: disable=unused-argument
    verbosity = 10 * (quiet - verbose)
    log_level = logging.WARNING + verbosity
    logging.basicConfig(level=log_level)
    LOGGER.info("Log level is set to %d.", log_level)

    LOGGER.info("Get problem name...")
    problem = os.getenv("PROBLEM")
    LOGGER.debug("problem = %s", problem)
    LOGGER.info("...Got")

    LOGGER.info("Receive a Solution as a JSON string...")
    in_json = input()
    LOGGER.debug("in_json = %s", in_json)
    LOGGER.info("...Received")

    LOGGER.info("Parse a Solution...")
    in_dict = json.loads(in_json)
    LOGGER.debug("in_dict = %s", in_dict)
    LOGGER.info("...Parsed")

    LOGGER.info("Load function...")
    func = load_function(problem)
    LOGGER.debug("func = %s", func)
    LOGGER.info("...Loaded")

    LOGGER.info("Validate a Solution...")
    validate_input(in_dict, func)
    LOGGER.info("...Validated")

    LOGGER.info("Evaluate a Solution...")
    out_dict = evaluate(in_dict, func)
    LOGGER.debug("out_dict = %s", out_dict)
    LOGGER.info("...Evaluated")

    LOGGER.info("Output the evaluation...")
    out_json = json.dumps(
        {
            "objective": out_dict["objective"],
            "constraint": out_dict["constraint"],
            "error": out_dict["error"],
            "info": out_dict["info"],
        }
    )
    LOGGER.debug("out_json = %s", out_json)
    print(out_json)


if __name__ == "__main__":
    try:
        LOGGER.info("Start")
        main(  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
            auto_envvar_prefix="HPA"
        )
        LOGGER.info("Successfully finished")
    except Exception as e:
        LOGGER.error(format_exc())
        out_json = json.dumps(
            {"objective": None, "constraint": None, "info": None, "error": str(e)}
        )
        print(out_json)
