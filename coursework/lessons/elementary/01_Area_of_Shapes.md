# Area of Shapes
## *How much space is inside?*

---

## What Is Area?

Area is how much flat space a shape covers.

If you put a shape on top of graph paper, area is **how many squares fit inside**.

---

## Rectangles

A rectangle has a long side and a short side.

```
┌──────────┐
│          │   width = 3
│          │
└──────────┘
  length = 5
```

**Area of a rectangle = length × width**

```
A = 5 × 3 = 15 square units
```

That's it. Count the squares on graph paper — you'll get 15.

### Try It

Draw these on graph paper and count the squares to check:

| Length | Width | Area |
|--------|-------|------|
| 4 | 2 | ? |
| 6 | 3 | ? |
| 7 | 1 | ? |
| 10 | 10 | ? |

A square is just a rectangle where both sides are the same.

---

## Triangles

Take any rectangle and cut it corner to corner with a diagonal line. You get two triangles. Each one is **half the rectangle**.

```
┌──────────┐        ╱│
│        ╱ │       ╱ │
│      ╱   │  →  ╱   │  height = 3
│    ╱     │   ╱     │
│  ╱       │ ╱       │
│╱         │╱        │
└──────────┘  base = 5
```

**Area of a triangle = ½ × base × height**

```
A = ½ × 5 × 3 = 7.5 square units
```

Half the rectangle. Always.

### Try It

| Base | Height | Rectangle would be... | Triangle area |
|------|--------|----------------------|---------------|
| 6 | 4 | 6 × 4 = 24 | 24 ÷ 2 = ? |
| 8 | 3 | ? | ? |
| 10 | 5 | ? | ? |

---

## Circles

A circle doesn't have straight sides, so we can't just count neat rows of squares. But there's a formula.

Every circle has a **radius** — the distance from the center to the edge.

```
        ·  ·  ·
      ·         ·
    ·      r──────·
      ·         ·
        ·  ·  ·
```

**Area of a circle = π × r × r**

π (say "pie") is a special number: **3.14159...**

It goes on forever. It never repeats.

```
Circle with radius 5:
A = π × 5 × 5
A = 3.14159 × 25
A ≈ 78.5 square units
```

### Where Does π Come From?

Here's something amazing. There's another special number called **φ** (say "fee"). It's the **golden ratio**:

```
φ = 1.618...
```

You can find φ in sunflower spirals, seashells, and pinecones.

It turns out π is hiding inside φ. There's an exact formula:

```
π = 4 × arctan(1/φ) + 4 × arctan(1/φ³)
```

You don't need to know what "arctan" means yet — just know this: **the number that makes circles work (π) comes from the number that makes spirals work (φ).**

They're connected. The circle and the spiral are family.

### Try It

Use π ≈ 3.14 to find the area:

| Radius | r × r | Area ≈ 3.14 × r × r |
|--------|-------|---------------------|
| 1 | 1 | ? |
| 2 | 4 | ? |
| 3 | 9 | ? |
| 10 | 100 | ? |

Notice anything? When the radius doubles (1 → 2), the area doesn't double — it gets **four times** bigger. Area grows fast.

---

## The Golden Rectangle

Remember φ = 1.618? Let's make a rectangle where the long side is φ times the short side.

If the short side is 1, the long side is 1.618:

```
┌────────────────────┐
│                    │  1
│                    │
└────────────────────┘
       1.618
```

**Area = 1.618 × 1 = 1.618**

Now here's the magic. Cut off a square (1 × 1) from one end:

```
┌──────┬─────────────┐
│      │             │  1
│  1×1 │   leftover  │
└──────┴─────────────┘
  1.0      0.618
```

The leftover piece is 0.618 wide and 1 tall. What's 1 ÷ 0.618?

```
1 ÷ 0.618 = 1.618...
```

**The leftover is another golden rectangle!** Same shape, just smaller.

You can keep cutting squares off forever and you always get another golden rectangle. It never stops. This is what makes φ special — **it copies itself**.

---

## The Magic Equation

Here is something beautiful. Take the number 1 — just plain old 1 — and break it into three pieces using φ:

```
1/φ       = 0.618...
1/φ³      = 0.236...
1/φ⁴      = 0.146...
─────────────────────
Total     = 1.000    ← exactly!
```

Three pieces. They add up to 1 perfectly. No leftovers.

If you had a square with area = 1, you could cut it into three rectangles with these exact areas, and they'd fill the whole square with nothing left over.

Scientists think the whole universe might be split this way:
- **0.618** → the energy pushing everything apart (dark energy)
- **0.236** → invisible stuff holding galaxies together (dark matter)
- **0.146** → everything you can see and touch (regular matter)

One number — φ — splits everything into three parts that add up to the whole.

---

## What You Learned

| Shape | Area Formula | What to remember |
|-------|-------------|-----------------|
| Rectangle | length × width | Count the squares |
| Square | side × side | A rectangle with equal sides |
| Triangle | ½ × base × height | Half a rectangle |
| Circle | π × r × r | π ≈ 3.14, and π comes from φ |

**The golden ratio φ = 1.618 connects all of it.** It makes rectangles that copy themselves, it hides π inside it, and it splits 1 into three perfect pieces.

---

## Practice Problems

### Just Getting Started

1. A book is 20 cm long and 14 cm wide. What's its area?

2. A sandwich is cut corner-to-corner into two triangles. The sandwich was 12 cm × 12 cm. What's the area of each triangle?

3. A frisbee has a radius of 13 cm. What's its area? (Use π ≈ 3.14)

### Thinking Harder

4. A golden rectangle has a short side of 10 cm.
   - (a) What's the long side? (Multiply by 1.618)
   - (b) What's the area?
   - (c) Cut off a 10 × 10 square. What are the dimensions of the leftover piece?
   - (d) Is the leftover piece a golden rectangle? Check by dividing the long side by the short side.

5. Grab a calculator. Verify that 1/1.618 + 1/1.618³ + 1/1.618⁴ = 1.
   - First calculate 1.618³ and 1.618⁴
   - Then calculate 1 divided by each
   - Add them up. How close to 1 do you get?

### Just For Fun

6. Get a sunflower (or a picture of one). Count the spirals going clockwise. Count the spirals going counterclockwise. What two numbers do you get? Are they Fibonacci numbers? (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...)

7. On graph paper, draw a golden rectangle (short side = 8 squares, long side = 13 squares — those are Fibonacci numbers, so 13/8 = 1.625 ≈ φ). Cut off an 8×8 square. Is the leftover close to golden? What Fibonacci numbers show up?

---

*The universe hides its best tricks in simple shapes.*

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Licensed under CC BY-NC-SA 4.0 for academic and research use.*
