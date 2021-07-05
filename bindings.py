import json
from typing import Optional, List, Union


class DirMeta:
    path: str
    disk_size: str
    num_files: int

    def __init__(self, path, disk_size, num_files):
        self.path = path
        self.disk_size = disk_size
        self.num_files = num_files

    def __str__(self):
        return f"directory path: {self.path}\ndisk size: {self.disk_size}\nfile count: {self.num_files}"


class LangStats:
    name: str
    loc: Optional[int]
    comments: Optional[int]

    def __init__(self, name, loc, comments):
        self.name = name
        self.loc = loc
        self.comments = comments

    def __str__(self):
        disp_val = f"\t{self.name}:"
        if self.loc is not None:
            disp_val += f"\n\tlines of code: {self.loc}"
        if self.comments is not None:
            disp_val += f"\n\tcommented lines: {self.comments}"
        return disp_val


class MediaMeta:
    file_name: str
    title: Optional[str]
    author: Optional[str]
    date: Optional[str]
    duration: Optional[str]
    stats: Optional[List[LangStats]]
    display_extra: bool
    extra: Optional[str]

    def __init__(self, file_name, title, author, date, duration, stats, display_extra, extra):
        self.file_name = file_name
        self.title = title
        self.author = author
        self.date = date
        self.duration = duration
        self.stats = stats
        self.display_extra = display_extra
        self.extra = extra

    def __str__(self):
        disp_val = f"{self.file_name}"
        if self.title is not None:
            disp_val += f"\ntitle: {self.title}"
        if self.author is not None:
            disp_val += f"\nauthor: {self.author}"
        if self.date is not None:
            disp_val += f"\ndate: {self.date}"
        if self.duration is not None:
            disp_val += f"\nduration: {self.duration}"
        if self.stats is not None:
            disp_val += f"\ncode breakdown:\n"
            disp_val += "\n\n".join([str(stat) for stat in self.stats])
        if self.display_extra and self.extra is not None:
            disp_val += f"\n{self.extra}"
        return disp_val


def parseBuoOutput(output: str) -> Union[MediaMeta, DirMeta, None]:
    inter = json.loads(output)

    try:
        if inter['stats'] is not None:
            stats = [LangStats(
                name=stat['name'],
                loc=stat['loc'],
                comments=stat['comments']
            ) for stat in inter['stats']]
        else:
            stats = None

        return MediaMeta(
            file_name=inter['file_name'],
            title=inter['title'],
            author=inter['author'],
            date=inter['date'],
            duration=inter['duration'],
            stats=stats,
            display_extra=inter['display_extra'],
            extra=inter['extra']
        )
    except KeyError:
        try:
            return DirMeta(
                path=inter['path'],
                disk_size=inter['disk_size'],
                num_files=inter['num_files']
            )
        except KeyError:
            pass

    return None
