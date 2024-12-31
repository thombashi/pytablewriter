"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import abc
from typing import IO, Any, Union


class TableWriterInterface(metaclass=abc.ABCMeta):
    """
    Interface class for writing a table.
    """

    @property
    @abc.abstractmethod
    def format_name(self) -> str:  # pragma: no cover
        """Format name for the writer.

        Returns:
            |str|
        """

    @property
    @abc.abstractmethod
    def support_split_write(self) -> bool:  # pragma: no cover
        """Indicates whether the writer class supports iterative table writing (``write_table_iter``) method.

        Returns:
            bool: |True| if the writer supported iterative table writing.
        """

    @abc.abstractmethod
    def write_table(self, **kwargs: Any) -> None:  # pragma: no cover
        """
        |write_table|.
        """

    def dump(
        self, output: Union[str, IO], close_after_write: bool, **kwargs: Any
    ) -> None:  # pragma: no cover
        raise NotImplementedError(f"{self.format_name} writer did not support dump method")

    def dumps(self) -> str:  # pragma: no cover
        raise NotImplementedError(f"{self.format_name} writer did not support dumps method")

    def write_table_iter(self, **kwargs: Any) -> None:  # pragma: no cover
        """
        Write a table with iteration.
        "Iteration" means that divide the table writing into multiple writes.
        This method is helpful, especially for extensive data.
        The following are the premises to execute this method:

        - set iterator to the |value_matrix|
        - set the number of iterations to the |iteration_length| attribute

        Call back function (Optional):
        A callback function is called when each iteration of writing a table is completed.
        You can set a callback function via the |write_callback| attribute.

        Raises:
            pytablewriter.NotSupportedError: If the writer class does not support this method.

        .. note::
            The following classes do not support this method:

                - |HtmlTableWriter|
                - |RstGridTableWriter|
                - |RstSimpleTableWriter|

            ``support_split_write`` attribute return |True| if the class
            is supporting this method.
        """

        self._write_table_iter(**kwargs)

    @abc.abstractmethod
    def _write_table_iter(self, **kwargs: Any) -> None:  # pragma: no cover
        pass

    @abc.abstractmethod
    def close(self) -> None:  # pragma: no cover
        pass

    @abc.abstractmethod
    def _write_value_row_separator(self) -> None:  # pragma: no cover
        pass
