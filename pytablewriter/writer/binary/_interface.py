import abc

from .._table_writer import AbstractTableWriter


class BinaryWriterInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_opened(self) -> bool:  # pragma: no cover
        pass

    @abc.abstractmethod
    def open(self, file_path: str) -> None:  # pragma: no cover
        """
        Open a file for output stream.

        Args:
            file_path (str): path to the file.
        """


class AbstractBinaryTableWriter(AbstractTableWriter, BinaryWriterInterface):
    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, value) -> None:
        raise RuntimeError(
            "cannot assign a stream to binary format writers. use open method instead."
        )

    def __init__(self) -> None:
        super().__init__()

        self._stream = None

    def dumps(self) -> str:
        raise NotImplementedError("binary format writers did not support dumps method")

    def _verify_stream(self) -> None:
        if self.stream is None:
            raise OSError("null output stream. required to open(file_path) first.")
