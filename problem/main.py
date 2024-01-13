import json
import logging
from os import path
from traceback import format_exc
from typing import Any, Mapping

import click
import yaml
from jsonschema import validate

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


# SHOULD implement your input validation
# sample schema
# type_var = "array"
# len_min_var = 10
# len_max_var = 10
# type_var_item = "number"
# val_min_var = 0
# val_max_var = 10
# type_add = "integer"
# val_min_add = 0
# val_max_add = 100
# INPUT_JSONSCHEMA = {
#     "$schema": "https://json-schema.org/draft/2020-12",
#     "title": "input schema",
#     "type": "object",
#     "properties": {
#         "variable": {
#             "type": type_var,
#             "minItems": len_min_var,
#             "maxItems": len_max_var,
#             "items": {
#                 "type": type_var_item,
#                 "minimum": val_min_var,
#                 "maximum": val_max_var
#             }
#         },
#         "add_info": {
#             "type": type_add,
#             "minimum": val_min_add,
#             "maximum": val_max_add
#         }
#     },
#     "additionalProperties": False,
#     "required": ["variable", "add_info"]
# }
def validate_input(input_obj: Any, schema) -> None:
    """入力された解を検証する

    説明を書く

    Parameters
    ----------
    input_obj :
        入力されたJSON文字列をパースして得られたオブジェクト．

    schema :
        入力レイアウトを規定するJSONスキーマ．strやdictで設定できる．

    Returns
    -------

    """

    if not schema:
        LOGGER.warning("Empty schema. Therefore, the input will not be validated.")
        return

    if isinstance(schema, str):
        validate(input_obj, json.loads(schema))
    else:
        validate(input_obj, schema)


# MUST implement evaluation
def calc_evaluation(input_obj: Any) -> Any:
    """解評価計算の本体

    説明を書く

    Parameters
    ----------
    input_obj :
        入力されたJSON文字列をパースして得られたオブジェクト．

    Returns
    -------
    Any
        解評価を表すPythonオブジェクト．

    Raises
    ------
    Exception
        解評価の異常終了を例外発生によって表現してもよい．
    """
    pass


# MUST format evaluation results
def format_output(out_obj: Any) -> Mapping[str, Any]:
    """計算結果の整形を行う

    説明を書く

    Parameters
    ----------
    out_obj:
        計算結果を表すPythonオブジェクト．

    Returns
    -------
    Mapping
        解の評価を表すMapping (dict)．この関数が例外を発生させることなく値を返す場合，次の4つのキーを必ず持つ必要がある．

        * `objective` : Optional[Union[float, list[float]]]
            目的関数値．異常終了時はNone．
        * `constraint`: Optional[Union[float, list[float]]]
            制約値．異常終了時はNone．
        * `error` : Optional[str]
            エラーメッセージ．正常終了時はNone．
        * `info` : Any
            追加情報．異常終了時はNone．

    Raises
    ------
    Exception
        解評価の異常終了を例外発生によって表現してもよい．
    """
    pass


# MUST wrap evaluation
def evaluate(input_obj: Any) -> Mapping[str, Any]:
    """入力された解を評価する

    説明を書く

    Parameters
    ----------
    input_obj :
        入力されたJSON文字列をパースして得られたオブジェクト．

    Returns
    -------
    Mapping
        解の評価を表すMapping (dict)．この関数が例外を発生させることなく値を返す場合，次の4つのキーを必ず持つ必要がある．

        * `objective` : Optional[Union[float, list[float]]]
            目的関数値．異常終了時はNone．
        * `constraint`: Optional[Union[float, list[float]]]
            制約値．異常終了時はNone．
        * `error` : Optional[str]
            エラーメッセージ．正常終了時はNone．
        * `info` : Any
            追加情報．異常終了時はNone．

    Raises
    ------
    Exception
        解評価の異常終了を例外発生によって表現してもよい．
    """

    LOGGER.info("Calculate on input...")
    out_obj = calc_evaluation(input_obj)
    LOGGER.debug("out_obj = %s", out_obj)
    LOGGER.info("...Calculated.")

    LOGGER.info("Format output...")
    out_formatted = format_output(out_obj)
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

    LOGGER.info("Receive a Solution as a JSON string...")
    in_json = input()
    LOGGER.debug("in_json = %s", in_json)
    LOGGER.info("...Received")

    LOGGER.info("Parse a Solution...")
    in_dict = json.loads(in_json)
    LOGGER.debug("in_dict = %s", in_dict)
    LOGGER.info("...Parsed")

    LOGGER.info("Validate a Solution...")
    validate_input(in_dict, {})  # SHOULD validate the input
    LOGGER.info("...Validated")

    LOGGER.info("Evaluate a Solution...")
    out_dict = evaluate(in_dict)
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
            auto_envvar_prefix="PROB"
        )
        LOGGER.info("Successfully finished")
    except Exception as e:
        LOGGER.error(format_exc())
        out_json = json.dumps(
            {"objective": None, "constraint": None, "info": None, "error": str(e)}
        )
        print(out_json)
