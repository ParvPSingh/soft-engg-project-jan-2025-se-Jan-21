## Week 1 - Lecture Transcripts

### A quick introduction to variables

Let us get back to our print command and type this statement, as you can see I say print 10,
when I execute this I see that 10 is being printed, displayed. Now, look at the small
modification that I do. I remove this 10 here, just above the print statement, I say a equals 10,
and then I include print a and what does this do? In mathematics we have observed this, we
always declare a variable, we say let us call a variable; let us assign the value 10 to it.
A computer also sees this as the letter a is assigned the value 10 and you are printing a, which
means whatever is assigned to this variable, will be printed here, as simple as that. So, when I
execute this I continue to get 10, here as you can see. Now, if I were to say b equals 20 and
then when I say print b, let me execute this.
I get print a, a gets printed here, print b, b gets printed here, which is 20. So, that is it, pretty
self-explanatory. What is the big deal about it? Now, look at this. I will say print a plus b, so
here is a plus b and then I say print a into b, I get a into b, which is 200, 10 times 200. Now,
let me delete all these things start afresh.

(Refer Slide Time: 1:58)

I will say a equals 10 as before and say print a, look at this, this is slightly counter intuitive. I
say a equals a plus 1. In mathematics what does it mean? This means you can cancel a and a
and 0 becomes equal to 1, which means this does not make sense in mathematics or the
conventional way in which we have learnt algebra, this statement really does not make sense,
but in computer science this is the most frequently used programming statement.
This simply means for the value of a, you take the existing value of a and add 1 to it, as
simple as that, the best way to see how something works is to execute the program and then
see it, so I have typed this program, it will of course, print the value of a here and then I do
something here and then print, let see what that something results in. It tells you 11, which
means the value of a right now is 11. Initially it was 10, now it is 11.

---

### Data types

Let us say we declare n equals 10 a variable n and then print the value of n. The output will
be as expected as you see the number 10. Assuming I take another number, let us say r equals
6.3 and then print r, obviously it will print first 10 and then will print r. Now, the point is
what if I said s equals, please note sudarshan, and then I will print s as well. So, you see what
is happening here?

Here is a number without any decimal value, here is a number with a decimal part. So, it is
not just an integer, it is a decimal, it is a fraction, 6.3, and then here this is neither an integer
nor is it a decimal number like this. This is a string, a name. I say print s and sudarshan gets
printed. Now the point is what we may want to note here is let me explain that with an
illustration.
When I say print type of n, you will see what this type does, you see it says class int, do not
worry about the, I would say it is a very ugly looking output, so with less than symbol,
greater then symbol, the word class and things like that, but all that it says is it is an integer
type number in n. What if we said print type r, executed, it says class float and then, so let me
just write this for clarity.
I will say the type, n is of type, let us say n is of type, then I say type r, make sense, r is of
type r. So, mind you the letter n here is not a variability, it is just, I am asking the computer to
print the whatever is inside the code, this n is not the value 10 here, this is simply the letter n,
which for reference let me just run this and show you, it will say n is of type class and r is of
type class float.
And then I say print s is of type, type s and I will execute this, you see what happens, s is of
type str, we have seen this somewhere before. So, str is string. What exactly does it mean?
What is int here, what is float here, what is str here? You never specified that anywhere here,
you went ahead and said n equals 10, r equals 6.3, s equals string sudarshan.
But the computer automatically called this as int type, integer, called this float, the word float
simply means something that is more than an integer, 10.171, now that is a floating point, it is
called a floating point number. So, in a first course in computing you will study all these
things, I am sure you did if not you can always look up, it is a very easy thing to understand.

---

### Variables and Literals

Hello Python students. In this lecture we will see variables and literals. In order to
demonstrate these concepts, we will use a Python code which is familiar to you. This is a
similar code which we saw in the previous lecture. Type your name, Sudarshan, type your
location, Mysore, then we will print message, ‘Hello Sudarshan, how is the weather in
Mysore?’ Then the next question is what is your age. Let us say 40. Good to know that you
are 40 years old.
Before moving to variables and literals let us see is it necessary to have print and input as two
separate commands or can we merge them together? To answer that question first we have to
understand what both these commands are doing. A print command is only printing a
message, whereas this particular input command is taking the input from the user and storing
it in n. This printing a message and taking a input can be combined together.

(Refer Slide Time: 1:33)

The same message we can place inside the brackets of input command and we can remove
this print. Let us execute, type your name, Sudarshan, type your location, Mysore, ‘Hello,
Sudarshan, how is the weather in Mysore. What is your age? You say 40. Good to know that
you are 40 years old. Still we are getting the same output. This is how we can merge print and
input together where we are displaying the message along with the input statement itself.

(Refer Slide Time: 2:29)

Now the next question is – is it necessary to have the name as Sudarshan, location as Mysore
and age as 40 or can we change the values. Let us try it. What is your name? Omkar. Type
your location, Pune. Hello, Omkar, how is the weather in Pune? That works. Let us see
whether next statement works. What is your age? Let us say 30. Good to know that you are
30 years old. Which means the same program

&#x20;executes perfectly with same messages even
though the values are changed.



## Week 2 - Lecture Transcripts

### Lecture 1
Here is an important tip that I am going to convey through a small program. So let us start
with this little story of two brothers, Ram and Lakshman. Let us say Ram’s bank balance is
one lakh and his bank loan, Ram’s bank loan is let us say 5 lakhs. Lakshman, his brother's
bank loan is, his brother's bank balance is let us say 20 lakhs and his bank loan is let us say
10 lakhs.
Do you observe something here? Is it not it indeed confusing to call it A, B, C and D? Is it
not important that we make the variables sort of self-explanatory? And that we need not
break our head on what exactly did I say just now? Was it bank balance or loan? Was it the
brother Ram or the brother Lakshman?
So it is easy if I were to simply name this as Ram bank balance, ram_bank_balance maybe
and then here instead of B I can say ram_loan. Instead of C I can say
lakshman_bank_balance. This character is called underscore that I am typing it looks like
dash but it is a little below dash at the line level and then I will say lakshman_loan. Now with
this it is sort of easy for me to calculate the, assuming that these two are brothers staying in

the same house and I would say the net income of the house is Ram's bank balance plus
Lakshman’s bank balance.

### Lecture 2
And let us say the net liability is what they owe. Ram’s loan plus Lakshman’s loan, makes
sense. Now, the final value let us say whatever that is, is net_income minus net_liability and I
will print the final value hoping that there are no errors right now. Let us see. So the final
value is 6 lakhs. So the family has, let us say, so the family has 6 lakhs.
(Refer Slide Time: 3:16)

Let me restart this kernel then we re-execute it. The so, the family has 6 lakhs. If let us say
Ram’s loan or let us say even Lakshman’s loan was a little more, then it would come 0 here
thus making it how much 10 lakh, 1 crore. So the family has minus 84 lakhs loan. So, if it is