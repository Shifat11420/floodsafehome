#You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

# You may assume the two numbers do not contain any leading zero, except the number 0 itself.

 

# Example 1:


# Input: l1 = [2,4,3], l2 = [5,6,4]
# Output: [7,0,8]
# Explanation: 342 + 465 = 807.
# Example 2:

# Input: l1 = [0], l2 = [0]
# Output: [0]
# Example 3:

# Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
# Output: [8,9,9,9,0,0,0,1]
 

# Constraints:

# The number of nodes in each linked list is in the range [1, 100].
# 0 <= Node.val <= 9
# It is guaranteed that the list represents a number that does not have leading zeros.


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

        
def add(data):
    newnode = ListNode(0)
    newnode.data = data
    newnode.next = None
    return newnode       
   
        
        
class Solution:
    def addTwoNumbers(self, l1, l2):
        
        # Function to convert the Linked List to an array
        def convertArr(head):
            arr = []

            index = 0
            curr = head

            # Traverse the Linked List and add the elements to the array one by one
            while (curr != None):
                arr.append( curr.val)
                curr = curr.next

            return arr
    

        list1 = convertArr(l1)
        list2 = convertArr(l2)

        #reverse list elements
        l1 = list(reversed(list1))
        l2 = list(reversed(list2))
        
        #list elements into string
        string_l1 = [str(int) for int in l1]             
        string_l2 = [str(int) for int in l2]  

        #join string
        str_of_l1 = "".join(string_l1)
        str_of_l2 = "".join(string_l2)

        #convert string to integer
        l1_num = int(str_of_l1)
        l2_num = int(str_of_l2)

        
        add_ = l1_num+l2_num
        add_str = str(add_)

        str_list = list(add_str)

        final_list = list(reversed(str_list))

        final_list = [int(each) for each in final_list]

        #convert list to linked list
        final_Llist = dummy = ListNode(0)

        for i in final_list:
            final_Llist.next = ListNode(i)
            final_Llist = final_Llist.next
        print(convertArr(dummy.next))
        return dummy.next    
#Solution().addTwoNumbers(l1,l2);