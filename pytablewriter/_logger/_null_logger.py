# encoding: utf-8


class NullLogger(object):
    level_name = None

    def catch_exceptions(self, *args, **kwargs):  # pragma: no cover
        pass

    def critical(self, *args, **kwargs):  # pragma: no cover
        pass

    def debug(self, *args, **kwargs):  # pragma: no cover
        pass

    def disable(self):  # pragma: no cover
        pass

    def enable(self):  # pragma: no cover
        pass

    def error(self, *args, **kwargs):  # pragma: no cover
        pass

    def exception(self, *args, **kwargs):  # pragma: no cover
        pass

    def info(self, *args, **kwargs):  # pragma: no cover
        pass

    def log(self, level, *args, **kwargs):  # pragma: no cover
        pass

    def notice(self, *args, **kwargs):  # pragma: no cover
        pass

    def warn(self, *args, **kwargs):  # pragma: no cover
        pass

    def warning(self, *args, **kwargs):  # pragma: no cover
        pass
