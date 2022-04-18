# AUTOGENERATED! DO NOT EDIT! File to edit: 00_magicdir.ipynb (unless otherwise specified).

__all__ = ['magicdir', 'extract_magicdir']

# Cell
from functools import wraps, partial
from pathlib import Path
from tarfile import ExtractError, TarFile
from io import BytesIO
from metaflow.client.core import MetaflowData

# Cell
def magicdir(_func=None, *, dir):
    artifact = 'magicdir'
    if _func is None: return partial(magicdir, dir=dir)
    @wraps(_func)
    def func(self):
        from io import BytesIO
        from tarfile import TarFile
        existing = getattr(self, artifact, None)
        Path(dir).mkdir(exist_ok=True)
        if existing:
            buf = BytesIO(existing)
            with TarFile(mode='r', fileobj=buf) as tar:
                tar.extractall()
        _func(self)
        buf = BytesIO()
        with TarFile(mode='w', fileobj=buf) as tar:
            tar.add(dir)
        setattr(self, artifact, buf.getvalue())
    return func

# Cell
def extract_magicdir(data:MetaflowData) -> None:
    "Extract `magicdir` into current directory."
    if not isinstance(data, MetaflowData):
        raise ValueError(f'data must be of type `MetaflowData, got {type(data)} instead')
    if not hasattr(data, 'magicdir'):
        raise ExtractError(f"Did not find magicdir attribute in metadata.")
    buf = BytesIO(data.magicdir)
    with TarFile(mode='r', fileobj=buf) as tar:
        tar.extractall()