# class Solution:
#     def isValid(self, s: str) -> bool:
#         # ()
#         hashmap = {
#                 ")":"(",
#                 "]":"[",
#                 "}":"{"
#                 }
#         stack = []
#         for char in s:
#             if char in hashmap and len(stack) > 0:
#                 if stack.pop() != hashmap[char]:
#                     return False
#             else:
#                 stack.append(char)
#         return len(stack) == 0
        
#         """
#         psudo code

#         consider eg: s = "([)]"
#         here hashmap is dic where closing brackets are used as keys
#         stack = []
#         for each char in s:
#             here s[0] = "("
#             "(" not in dic and len(stack) is not greater than 0
#             so else part
            
#             stack = ["("]
            
#             now again
            
#             [ not in hasmap and len(stack) == 1 ie 1>0 
                
#             so append 
#             stack = ["(","["]
            
#             now again loop
            
#             ) in hashmap true 2<0:
#             if stack.pop() which is [ is not equal to hashmap[char] ir [ != )
            
#             so return false 
            
#             same for all test cases
            
#         """
#     def isValid_(self, s: str) -> bool:

#         # assert even number
#         if len(s) % 2 == 1:
#             return False

#         # 0 1 2 3
#         # ( { } )
#         # -4 -3 -2 -1

#         opposition = {
#                 '(':')',
#                 '{':'}',
#                 '[':']',
#         }

#         # algorithm
#         # left = first char
#         # find its pairing
#         # check its inclusive and pop out
#         # loop next pairing

#         def inclusive(s):
#                 # ()
#                 # ([])
#                 # ({[]})
                
#                 while True:
#                     if s == '':
#                         return True
#                     cut_index = cut_a_inclusive(s)
#                     if cut_index == False:
#                         return False
#                     # ({})[{{}}] => [{{}}]
#                     # cut_index = 3
#                     s = s[cut_index+1:]  # => [{{}}]

                        
                
#                 # check inclusive
#                 for i in range(int(len(s)/2)):
#                         # i => 0
#                         # -i-1 => -1

#                         # i => 1
#                         # -i-1 => -2

#                         # i => 2
#                         # -i-1 => -3

#                         left = s[i]
#                         right = s[-i-1]
#                         if left not in opposition:
#                                 return False
#                         if opposition[left] != right:
#                                 return False
#                 return True

#         def get_cut_index(s, its_opposition):
# #                 # find index of its opposition => cut_index
# #                 cut_index = 1
# #                 while True:
# #                         if cut_index >= len(s):
# #                                 return None

# #                         char = s[cut_index]
# #                         if char == its_opposition:
# #                                 break
# #                         cut_index += 1

# #                 return cut_index
        
# #         # cut out inclusive
# #         # ()[()] => (), [()] => True
# #         # (])[] => (]), [] => False
# #         def cut_a_inclusive(s):
# #                 first_char = s[0] # (
# #                 if first_char not in opposition:
# #                         return False
# #                 its_opposition = opposition[first_char] # )
# #                 cut_index = get_cut_index(s, its_opposition)
# #                 if cut_index == None:
# #                         return False

# #                 # set data for check inclusive
# #                 # s = ([]){}
# #                 my_str = s[:cut_index+1] #[0:4] => ([])

# #                 result = inclusive(my_str)
# #                 if result == False:
# #                         return False
# #                 return cut_index

# #         while True:
# #                 if s == '':
# #                         return True
# #                 cut_index = cut_a_inclusive(s)
# #                 if cut_index == False:
# #                         return False
# #                 # ({})[{{}}] => [{{}}]
# #                 # cut_index = 3
# #                 s = s[cut_index+1:] # => [{{}}]
                


    

# #     def test_case(self, s):
# #         result = self.isValid(s)
# #         print('your input =', [s], 'result=', [result])
# #         return result


# # solution = Solution()
# # assert solution.test_case("()")==True
# # assert solution.test_case("()[]")==True
# # assert solution.test_case("(")== False
# # assert solution.test_case("()]") ==False
# # assert solution.test_case("()[{}]") ==True
# # assert solution.test_case("(){}}{") == False
# # assert solution.test_case("(([]){})") == True
# # print('success')

# # def test_key(f_arg, pos_arg, *args, **kk):
# #     print('my name is:', f_arg)
# #     print(len(args), 'len args')
# #     print(len(kk), 'len kk')
# #     print('---kk', kk)
# #     for arg in args:
# #         print('I am a', arg)

# # test_key('o', 'dog', 'bird', 'cat')

# arr = [0,0,0,1,1,1]
# # arr = [0,0,0,0,0,0]
# n = len(arr)

# def transitionPoint(arr, n):
#     #Code here
#     for i in range(n):
#         print('--',i)
#         #find the transition point with len
#         #return the len that make the transition
#         if (arr[i] >= 1):
#             return i 
    
#     return -1

# point = transitionPoint(arr,n)
# if point >= 0:
#     print(point)
# else:
#     print('no transition point')

# a = 5
# for i in [3,7,9]:
#     a = i 
# print(a)

# arr = {1, 8, 7, 56, 90}
# # sorted(arr)
# l = list(arr)
# l.sort()

# # sorted(arr)
# print(l[-1])


# def largest( arr, n):
#     max = arr[0]
    
#     for i in arr:
#         if i > max:
#             max = i
            
#     return max

# def test(arr, n, gt):
#     ans = largest(arr, n)
#     print('-----------',ans, gt)
#     assert ans==gt

# test([1,2,3,4,10,50,30], 7, 50)
a = 1
if a == 1:
    print('in')
else:
    print('out')
