class Node(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def sumOfLeftLeaves(self, root):
        """
        root: Node
        return type: int
        """
        ans_sum = 0
        #print root.val
        if root == None:
            return ans_sum
        if root.left != None:
            if root.left.right == None and root.left.left == None:
                ans_sum += root.left.val
            else:
                ans_sum += self.sumOfLeftLeaves(root.left)
        if root.right != None:
            ans_sum += self.sumOfLeftLeaves(root.right)
        return ans_sum


if __name__ == '__main__':
    # if there is only one root, is this count for left leaf
    # test 1
    root = Node(20)
    root.left = Node(9)
    root.right = Node(49)
    root.left.left = Node(5)
    root.left.right = Node(12)
    root.left.right.right = Node(15)
    root.right.left = Node(23)
    root.right.right = Node(52)
    root.right.right.left = Node(50)
    sol = Solution()
    print(sol.sumOfLeftLeaves(root))