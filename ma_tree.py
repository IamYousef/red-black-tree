r"""
Tree in __doc__s are genrated by https://github.com/joowani/binarytree/blob/master/binarytree
"""

# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, missing-function-docstring, missing-class-docstring, trailing-newlines, trailing-whitespace


import sys
import warnings
from ma_node import BasicNode, Color


class RBT:
    """
    A red-black tree is a kind of self-balancing binary search tree where each 
    node has an extra bit, and that bit is often interpreted as the color (red or black). 
    These colors are used to ensure that the tree remains balanced during insertions and deletions. 
    Although the balance of the tree is not perfect, it is good enough to reduce the 
    searching time and maintain it around O(log n) time, where n is the total number
    of elements in the tree.
    """

    _basic_node = BasicNode
    _cls_name = "RBT"

    def __init__(self, iterable=None):
        r"""class method which creates a `RBT()` instance using an
        iterable in time-complexity of O(n) where * n * is the number of
        elements inside the given `iterable`.

        Args:
            iterable: iterable (default: None)
            An iterable python object that implements the `__iter__` method.

        Raises:
            TypeError:
                * In case the given object isn't iterable.
                * If one of the elements in the iterable is NOT a number.

            ValueError: If one of the iterable elements is `None`.

        Examples:
        >>> exp = RBT([13, 8, 17, 1, 11, 15, 25, 6])
        >>> exp
                   ______13|B______
                  /                \
           _____8|R_             __17|B_
          /         \           /       \
        1|B_        11|B      15|R      25|R
            \
            6|R

        Using an iterable object with `None` as one of its elements will raise
        `ValueError`

        >>> RBT([2, None])
        ValueError: Can't use `None` as an element within
        `RBT()`

        Using a non-iterable object will raise `TypeError`

        >>> RBT(2)
        TypeError: The given object isn't iterable

        Using nested `RBT()` objects will raise `TypeError` as well

        >>> exp_1 = RBT([1])
        >>> exp_2 = RBT([1, exp_1])
        TypeError: Can't create `RBT` using `RBT`
        """
        self.root = None
        self._length = 0

        if iterable is None:
            return
        if not hasattr(iterable, "__iter__"):
            raise TypeError("The given object should be iterable")

        for item in iterable:
            self.insert(item)

    # >>>-insertion-methods--->
    def _insert_node(self, start_node, inserted_node):
        """
        Inserts a `Node()` in the subtree whose root is `start_node`
        according to the rules of binary search trees.

        Args:
        ----------
        start_node: Node()
            The root of the subtree where the new node will be inserted.
        inserted_node: Node()
            The new node that will be inserted

        Returns
        -------
        Node():
            A reference to the new node after being inserted to the subtree.

        Raises
        ------
        AssertionError:
            This will be raised in the following cases:
                1. If `start_node` isn't an instance of `Node()`.
                2. If the `inserted_node` is not either `None` nor an
                instance of `Node()`.
        """
        assert isinstance(start_node, self._basic_node)
        assert (
            inserted_node is None
            or isinstance(inserted_node, self._basic_node)
        )

        value = inserted_node.get_data()
        if value == start_node.get_data():
            warnings.warn(
                f"`{value}` already exists in `{self._cls_name}`", UserWarning
            )
            return start_node
        elif value < start_node.get_data():
            if start_node.get_left():
                # check if left of the given is already exist
                return self._insert_node(start_node.get_left(), inserted_node)
            else:
                start_node.set_left(inserted_node)
                self._length += 1
                return inserted_node
        else:
            if start_node.get_right():
                # check if right of the given is already exist
                return self._insert_node(start_node.get_right(), inserted_node)
            else:
                start_node.set_right(inserted_node)
                self._length += 1
                return inserted_node

    def _insert_numeric(self, start_node, value):
        """
        Inserts a numeric value in the subtree whose root is `start_node`
        according to the rules of binary search trees.

        Args:
        ----------
        start_node: Node()
            The root of the subtree where the new node will be inserted.
        value: int or float
            The new numeric value that will be inserted.

        Returns
        -------
        Node():
            A reference to the new node after being inserted to the subtree.

        Raises
        ------
        AssertionError:
            This will be raised in the following cases:
                1. If `start_node` isn't an instance of `Node()`.
                2. If the given `value` is not a numeric value.

        """
        assert isinstance(start_node, self._basic_node)
        assert type(value) in {float, int}

        inserted_node = self._basic_node(value)
        return self._insert_node(start_node, inserted_node)

    def _insert(self, value):
        """
        Inserts a numeric value in the `RBT()` instance according to the rules
        of binary search trees.

        Args:
        ----------
        value: int or float
            The new numeric value that will be inserted.

        Returns
        -------
        Node():
            A reference to the new node after being inserted to the subtree.

        Raises
        ------
        AssertionError:
            If the given `value` is not a numeric value.
        """
        assert (
            type(value) in {int, float}
            or isinstance(value, self._basic_node)
        )

        if isinstance(value, self._basic_node):
            # if the given value is instance of Node
            return self._insert_node(self.root, value)
        else:
            # if the given value is instance of int | float
            return self._insert_numeric(self.root, value)

    def insert(self, value):
        """
        Inserts a numeric value in the `RBT()` instance according to
        the rules of binary search trees and the rules red-black trees as well.

        Args:
        ----------
        value: int or float
            The new numeric value that will be inserted.

        Raises
        ------
        ValueError:
            If the given `value` is `None`.
        TypeError:
            If either the given `value` is not a numeric value.

        Example
        -------
        >>> exp = RBT()
        >>> exp.insert(10)
        >>> exp.insert(5)
        >>> exp.insert(15)
        >>> exp
           _10|B_
          /      \\
        5|R      15|R
        >>> exp.insert("2")
        TypeError: `RBT` accepts only numbers
        """
        if value is None:
            raise ValueError(
                f"Can't use `None` as an element within `{self._cls_name}`!!"
            )

        if self.is_empty():
            self.root = self._basic_node(value)
            self.root.set_color(Color.BLACK)
            self._length += 1
        else:
            # insert new node
            new_node = self._insert(value)
            # recolor starting from new_node till root
            self.root = self._recolor(new_node)
            # root is always black (isn't essential tho)
            self.root.set_color(Color.BLACK)

    # >>>-Rotations--->
    def _rotate_left(self, start_node):
        """
        Rotates the given subtree whose root is `start_node` to the left side.

        Args:
        ----------
        start_node: Node()
            A reference to the root of the subtree that will be rotated

        Returns
        -------
        Node():
            A reference to the new root fo the subtree after rotation.

        Raises
        ------
        AssertionError:
            If the given `start_node` is not `Node()`.

        Example
        -------
        >>> RBT = RBT([1, 2, 3])
        >>> RBT
        1
         \\
          2
           \\
            3
        >>> RBT.root = RBT._rotate_left(RBT.root)
        >>> RBT
          2
         / \\
        1   3
        """
        assert isinstance(start_node, self._basic_node)

        # print("Rotating Left")
        middle = start_node.get_right()
        middle.set_parent(start_node.get_parent())
        start_node.set_right(middle.get_left())
        middle.set_left(start_node)
        return middle

    def _rotate_right(self, start_node):
        """
        Rotates the given subtree whose root is `start_node` to the right side.

        Args:
        ----------
        start_node: Node()
            A reference to the root of the subtree that will be rotated

        Returns
        -------
        Node():
            A reference to the new root fo the subtree after rotation.

        Raises
        ------
        AssertionError:
            If the given `start_node` is not `Node()`.

        Example
        -------
        >>> RBT = RBT([3, 2, 1])
        >>> RBT
            3
           /
          2
         /
        1
        >>> RBT.root = RBT._rotate_right(RBT.root)
        >>> RBT
          2
         / \\
        1   3
        """
        assert isinstance(start_node, self._basic_node)

        # print("Rotating Right")
        middle = start_node.get_left()
        middle.set_parent(start_node.get_parent())
        start_node.set_left(middle.get_right())
        middle.set_right(start_node)
        return middle

    # >>>-Re-Branding-aka-re-coloring--->
    def __recolor_case3(self, start_node):
        """
        Recolors the `RBT()` instance when the parent of the given
        `start_node` is 'red' and uncle is 'black'. Case III

        Args:
        ----------
        start_node: Node()
            A reference to the root of the subtree at which recoloring begins.

        Returns
        -------
        Node():
            A reference to the same given `start_node` after recoloring the
            whole subtree.

        Raises
        ------
        AssertionError:
            If the given `start_node` isn't a `Node()`.
        """
        assert isinstance(start_node, self._basic_node)

        # get basic info
        parent = start_node.get_parent()
        grandparent = parent.get_parent() if parent else None
        # parent is left-child and start_node is left-child
        if parent.is_left_child() and start_node.is_left_child():
            grandparent.set_color(Color.RED)
            parent.set_color(Color.BLACK)
            grandparent = self._rotate_right(grandparent)
        # parent is left-child and start_node is right-child
        elif parent.is_left_child() and not start_node.is_left_child():
            # first rotation
            parent = self._rotate_left(parent)
            grandparent.set_left(parent)
            grandparent.set_color(Color.RED)
            # second rotation
            grandparent = self._rotate_right(grandparent)
            grandparent.set_color(Color.BLACK)
        # parent is right-child and start_node is left-child
        elif not parent.is_left_child() and start_node.is_left_child():
            # first rotation
            parent = self._rotate_right(parent)
            grandparent.set_right(parent)
            grandparent.set_color(Color.RED)
            # second rotation
            grandparent = self._rotate_left(grandparent)
            grandparent.set_color(Color.BLACK)
        # parent is right-child and start_node is right-child
        else:
            grandparent.set_color(Color.RED)
            parent.set_color(Color.BLACK)
            grandparent = self._rotate_left(grandparent)
        return grandparent
    
    def _recolor(self, start_node):
        """
        src: https://youtu.be/5IBxA-bZZH8

        Recolors the `RBT()` instance after insertion or removal(not implemented). When
        recoloring, there are three different cases that can be discussed:

        - case I:   parent is 'black'
        - case II:  parent is 'red' and uncle is 'red'
        - case III: parent is 'red' and uncle is 'black'

        Args:
        ----------
        start_node: Node()
            A reference to the root of the subtree at which recoloring begins.

        Returns
        -------
        Node():
            A reference to the same given `start_node` after recoloring the
            whole subtree.

        Raises
        ------
        AssertionError:
            If the given `start_node` isn't a `Node()`.
        """
        assert isinstance(start_node, self._basic_node)

        # basic info
        uncle = start_node.get_uncle()
        parent = start_node.get_parent()
        grandparent = parent.get_parent() if parent else None
        # recolor when node has a grandparent
        if parent is None or grandparent is None:
            return parent if parent else start_node

        # case I
        if parent.get_color() == Color.BLACK:
            # do nothing
            # return("Case I")
            return self.root
        else:
            # case II
            # if uncleexist and its color is red
            if uncle and uncle.get_color() == Color.RED:
                # return("Case II")
                parent.set_color(Color.BLACK)
                uncle.set_color(Color.BLACK)
                grandparent.set_color(Color.RED)
            # case III
            else:
                # return("Case III")
                # get great grandparent
                great_grandparent = grandparent.get_parent()
                grandparent = self.__recolor_case3(start_node)
                # set connection
                if great_grandparent:
                    if great_grandparent.get_data() > grandparent.get_data():
                        great_grandparent.set_left(grandparent)
                    else:
                        great_grandparent.set_right(grandparent)
            # recursively do the same over grandparent
            return self._recolor(grandparent)

    # >>>-Helpers--->
    def is_empty(self):
        """
        Checks if the `RBT()` instance is empty or not in constant
        time.

        Returns
        -------
        bool:
            A boolean flag showing if the `RBT` instance is empty or
            not. `True` shows that this instance is empty and `False` shows
            it's not empty.

        Example
        --------
        >>> exp = RBT
        >>> exp.is_empty()
        True
        >>> exp.insert(10)
        >>> exp.is_empty()
        False
        """
        return self.root is None

    def _print_me(self, node, indent, last):
        if node is not None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            
            print(node.represent_color())
            self._print_me(node._left, indent, False)
            self._print_me(node._right, indent, True)

    def print_tree(self):
        return self._print_me(self.root, "", True)

    
    
exp = RBT([13, 8, 17, 1, 11, 15, 25, 6])
exp.print_tree()