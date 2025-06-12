from pydantic import RootModel


class Balance(RootModel):
    root: dict[str, int]
