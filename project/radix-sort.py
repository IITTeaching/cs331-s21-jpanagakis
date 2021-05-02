import urllib
import requests

def radixSort(arr):
    maximum = len(max(arr,key=len))-2
    output = countSort(arr,maximum+1)
    for i in range(maximum,-1,-1):
        output = countSort(output, i)
    return output

def countSort(arr, place):
    count = [0] * 128
    output = [None] * len(arr)
    for i in arr:
        if len(i)-1 < place:
            key = 0
        else:
            key = ord(i.decode('ascii')[place])
        count[key] += 1
    
    for i in range(1,len(count)):
        count[i] += count[i-1]
    
    for i in range(len(arr)-1,-1,-1):
        if len(arr[i])-1 < place:
            key = 0
        else:
            key = ord(arr[i].decode('ascii')[place])
        output[count[key]-1] = arr[i]
        count[key] += -1
    return output

def book_to_words(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii','replace')
    return bookascii.split()

def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    return radixSort(book_to_words())
