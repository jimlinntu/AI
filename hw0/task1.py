def twoSum(nums, target):
    ans = []
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                ans.append(i)
                ans.append(j)
                return ans
if __name__ == '__main__':
    nums = [0, 7, 11, 15, 60, 30, 10]
    ans = twoSum(nums, 40)
    print ans