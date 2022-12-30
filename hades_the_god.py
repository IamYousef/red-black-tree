r"""House Of Hades is just silly name to have a base class for everything in this project
"""
# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, missing-function-docstring, missing-class-docstring
class HouseOfHades:
    _cls_name = "THEROOT"
    def adjudging(self, case) -> None:
        if case is None:
            raise ValueError(
                f"Can't use `None` as an element within `{self._cls_name}`!!"
            )
        elif isinstance(case, HouseOfHades):
            raise TypeError(
                f"Can't use `{self._cls_name}` with `{case._cls_name}`!!"
            )
