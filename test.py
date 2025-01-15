class Book:
    def __init__(self, title, author):
        self._title = title
        self._author = author

    def __str__(self):
        return f"'{self._title}' by {self._author}"


class Team:
    def __init__(self, team_list):
        self._team_list = team_list

    def __gt__(self, other):
        if isinstance(other, Team):
            return len(self._team_list) > len(Team._team_list)
        else:
            raise Exception("One of the object is not an instance of class Team")

    def __lt__(self, other):
        if isinstance(other, Team):
            return len(self._team_list) < len(Team._team_list)
        else:
            raise Exception("One of the object is not an instance of class Team")

    def __eq__(self, other):
        if isinstance(other, Team):
            return len(self._team_list) == len(Team._team_list)
        else:
            raise Exception("One of the object is not an instance of class Team")


class Cart:
    def __init__(self, item_list):
        if isinstance(item_list, list):
            self._item_list = item_list
        else:
            raise Exception("input parameter is not a list")

    def __len__(self):
        return len(self._item_list)


class Rectangle:
    def __init__(self, width, height):
        if isinstance(width, int or float) and width > 0:
            self._width = width
        else:
            raise Exception("invalid width")
        if isinstance(height, int or float) and height > 0:
            self._height = height
        else:
            raise Exception("invalid height")

    def __lt__(self, other):
        if isinstance(other, Rectangle):
            return self._width * self._height < other._width * other._height
