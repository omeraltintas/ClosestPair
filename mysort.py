#Merge Sort will be used in closest pair project divide and conquer approach
def merge(left,right,key):
    result=[]
    i=0
    j=0
    while i<len(left)and j<len(right):
        if key(left[i])<=key(right[j]):
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+=1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(arr,key=lambda x: x):
    if len(arr)<=1:
        return arr
    mid=len(arr)//2
    left=merge_sort(arr[:mid],key)
    right=merge_sort(arr[mid:],key)
    return merge(left,right,key)



