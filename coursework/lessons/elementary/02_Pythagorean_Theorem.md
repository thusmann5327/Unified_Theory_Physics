# The Pythagorean Theorem
## *The rule that every right triangle follows — and why it matters*

---

## What's a Right Triangle?

A right triangle has one corner that makes a perfect square corner — a 90° angle. Like the corner of a book or a door frame.

```
        ╱|
      ╱  |
    ╱    |  b
  ╱      |
╱________|
    a
```

The two sides that touch the square corner are called **legs** (a and b).

The long side across from the square corner is called the **hypotenuse** (c). It's always the longest side.

```
        ╱|
    c ╱  |
    ╱    |  b
  ╱      |
╱________|
    a
```

---

## The Rule

**a² + b² = c²**

That's it. The two short sides squared, added together, equal the long side squared.

"Squared" just means multiplied by itself:
- 3² = 3 × 3 = 9
- 4² = 4 × 4 = 16
- 5² = 5 × 5 = 25

### The Famous 3-4-5 Triangle

```
a = 3     →  3² = 9
b = 4     →  4² = 16
                   ──
             9 + 16 = 25

c² = 25   →  c = 5  ✓
```

Does it work? 3² + 4² = 9 + 16 = 25 = 5². **Yes.**

### See It With Squares

Draw actual squares on each side of the triangle:

```
         ┌─┬─┬─┬─┬─┐
         │ │ │ │ │ │
         ├─┼─┼─┼─┼─┤
         │ │ │ │ │ │    5 × 5 = 25
         ├─┼─┼─┼─┼─┤
    ╱──  │ │ │ │ │ │
  ╱   │  ├─┼─┼─┼─┼─┤
╱  c  │  │ │ │ │ │ │
      │  ├─┼─┼─┼─┼─┤
      │  │ │ │ │ │ │
  ┌─┬─┬─┐└─┴─┴─┴─┴─┘
  │ │ │ │
  ├─┼─┼─┤  ┌─┬─┬─┬─┐
  │ │ │ │  │ │ │ │ │
  ├─┼─┼─┤  ├─┼─┼─┼─┤
  │ │ │ │  │ │ │ │ │  4 × 4 = 16
  └─┴─┴─┘  ├─┼─┼─┼─┤
  3×3 = 9  │ │ │ │ │
            ├─┼─┼─┼─┤
            │ │ │ │ │
            └─┴─┴─┴─┘
```

Count the small squares: 9 + 16 = 25. The two smaller squares **fit exactly** into the big one.

---

## Try It Yourself

Find the missing side:

| a | b | a² | b² | a² + b² | c |
|---|---|----|----|---------|---|
| 3 | 4 | 9 | 16 | 25 | 5 |
| 6 | 8 | ? | ? | ? | ? |
| 5 | 12 | ? | ? | ? | ? |
| 8 | 15 | ? | ? | ? | ? |

**Hint for the last one:** 64 + 225 = ?. Then find a number that, multiplied by itself, gives that answer.

---

## Going Backwards — Finding a Leg

What if you know the hypotenuse and one leg?

Say c = 10 and a = 6. What's b?

```
a² + b² = c²
6² + b² = 10²
36 + b² = 100
b² = 100 - 36 = 64
b = 8
```

Check: 6² + 8² = 36 + 64 = 100 = 10² ✓

---

## The Circle Connection

Here's something cool. Every point on a circle follows the Pythagorean theorem.

Put a circle with radius r at the center of a grid. Pick any point on the circle. Call its position (x, y).

```
        y
        │     · (x, y)
        │   ╱
        │ ╱  r
        │╱
   ─────┼──────── x
        │
```

The distance from the center to that point is r. And:

**x² + y² = r²**

That's the Pythagorean theorem! The x-distance is one leg, the y-distance is the other leg, and the radius is the hypotenuse.

**A circle IS the Pythagorean theorem, drawn in every direction at once.**

That's why the area of a circle uses r² — because r is the hypotenuse of every tiny right triangle you can make from the center to the edge.

---

## The Golden Ratio Connection

Remember φ = 1.618 from the area lesson? Watch what happens with the Fibonacci numbers:

```
Fibonacci: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...
```

Each number is the sum of the two before it. Now look at these three numbers:

```
5, 8, 13
```

They're right next to each other in the Fibonacci sequence. And:

```
(√5)² + (√8)² = (√13)²

5 + 8 = 13  ✓
```

**That's a Pythagorean relationship!** The square roots of three Fibonacci numbers in a row make a right triangle.

The legs are √5 ≈ 2.24 and √8 ≈ 2.83. The hypotenuse is √13 ≈ 3.61.

### Why This Matters

The ratio of the hypotenuse to the short leg is:

```
√13 / √5 = √(13/5) = √2.6 ≈ 1.612
```

That's really close to φ = 1.618. The golden ratio is hiding in this triangle.

And here's the deepest part: there is no "fourth side" that keeps this pattern going. The next Fibonacci number after 5, 8, 13 is 21. But:

```
8 + 13 = 21    ← Fibonacci works
(√8)² + (√13)² = 8 + 13 = 21
(√21)² = 21    ← Pythagorean works too!

But going further:
13 + 21 = 34   ← Fibonacci still works
(√13)² + (√21)² = 13 + 21 = 34
(√34)² = 34    ← Still Pythagorean...

Wait — it always works?!
```

Actually, the *Fibonacci addition* always works (that's just what Fibonacci numbers do). But the special thing about 5, 8, and 13 is that they are the **discriminants** of the three most important metallic ratios in nature:

- **5** goes with the golden ratio φ (sunflowers, pinecones)
- **8** goes with the silver ratio (paper sizes, octagonal tiles)
- **13** goes with the bronze ratio (how those two combine)

After these three, the pattern changes. There's no fourth natural ratio that fits the same way. That's connected to why we live in a world with **three** directions (left-right, forward-back, up-down) and not four.

Three dimensions. Three Fibonacci discriminants. One Pythagorean theorem linking them together.

---

## Real Life Uses

### How Far Away Is It?

You're standing 30 meters from a building. The building is 40 meters tall. How far is it from your feet to the top of the building?

```
        │ 40 m
        │
        │
you ────┘
  30 m

c² = 30² + 40²
c² = 900 + 1600
c² = 2500
c = 50 meters
```

### Screen Sizes

TV screens are measured diagonally — that's the hypotenuse! A screen that's 48 inches wide and 27 inches tall:

```
c² = 48² + 27²
c² = 2304 + 729
c² = 3033
c ≈ 55 inches
```

That's a 55-inch TV.

---

## Practice Problems

### Just Getting Started

1. Find the hypotenuse:
   - a = 5, b = 12
   - a = 9, b = 12
   - a = 7, b = 24

2. Find the missing leg:
   - a = 5, c = 13 → b = ?
   - b = 8, c = 17 → a = ?

3. A ladder leans against a wall. The bottom of the ladder is 6 feet from the wall. The top reaches 8 feet up the wall. How long is the ladder?

### Thinking Harder

4. On graph paper, draw a circle by plotting all the points where x² + y² = 25. (Hint: find the points where x or y equals 0, 3, 4, or 5.)

5. Verify that √5, √8, √13 make a right triangle:
   - Calculate (√5)² + (√8)²
   - Calculate (√13)²
   - Are they equal?
   - Now calculate √13 ÷ √5. How close to φ = 1.618 do you get?

6. A golden rectangle has sides 1 and 1.618. What's the length of its diagonal?
   - Use a² + b² = c²
   - Calculate 1² + 1.618²
   - Take the square root
   - **Bonus:** Divide your answer by 1.618. What do you notice?

### Just For Fun

7. The 3-4-5 triangle is the smallest Pythagorean triple with whole numbers. The next few are 5-12-13 and 8-15-17. Can you find one more? (Hint: try a = 7.)

8. Stand in your room. Measure the length of the floor, the width, and then walk diagonally corner to corner. Does the Pythagorean theorem predict the diagonal? Measure and check!

---

## What You Learned

| Idea | What it means |
|------|--------------|
| a² + b² = c² | The two short sides of a right triangle, squared and added, equal the long side squared |
| Hypotenuse | The long side, across from the right angle |
| x² + y² = r² | A circle is the Pythagorean theorem in every direction |
| 5 + 8 = 13 | Fibonacci numbers make a Pythagorean triple — and this is connected to why we have three dimensions |

**One rule — a² + b² = c² — connects triangles, circles, distances, and the shape of space itself.**

---

*The universe is built on right angles and golden spirals. Now you know the rule that holds them together.*

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Licensed under CC BY-NC-SA 4.0 for academic and research use.*
