import random
import string

def makeRandomPassword(length=20, chars=string.letters + string.digits):
  return ''.join( random.Random().sample(chars, length) )
