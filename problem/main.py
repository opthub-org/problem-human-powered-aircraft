import json
import logging
from traceback import format_exc

from jsonschema import validate
import click

LOGGER = logging.getLogger(__name__)

# [優先度: 中] 検証用のスキーマを設定する
# sample
type_var = "array"
len_min_var = 10
len_max_var = 10
type_var_item = "number"
val_min_var = 0
val_max_var = 10
type_add = "integer"
val_min_add = 0
val_max_add = 100
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
        },
        "add_info": {
            "type": type_add,
            "minimum": val_min_add,
            "maximum": val_max_add
        }
    },
    "additionalProperties": False,
    "required": ["variable", "add_info"]
}


# [優先度: 高] ここに解評価を実装する
def evaluate(input: dict) -> dict:
    pass


@click.option("-q", "--quiet", count=True, help="Be quieter.")
@click.option("-v", "--verbose", count=True, help="Be more verbose.")
@click.pass_context
def main(ctx, quiet, verbose):
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
    # validate(in_dict, INPUT_JSONSCHEMA)  # [優先度: 中] ここで入力の検証を行う
    LOGGER.info("...Validated")

    LOGGER.info("Evaluate a Solution...")
    out_dict = evaluate(in_dict)
    LOGGER.debug("out_dict = %s", out_dict)
    LOGGER.info("...Evaluated")

    LOGGER.info("Output the evaluation...")
    out_json = json.dumps({
        "objective": out_dict["objective"],
        "constraint": out_dict["constraint"],
        "error": None,
        "info": out_dict["info"]
    })
    LOGGER.debug("out_json = %s", out_json)
    print(out_json)


if __name__ == '__main__':
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
