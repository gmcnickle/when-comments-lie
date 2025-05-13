
# *When Comments Lie*: Django .all() -vs- .first()

> “The proper use of comments is to compensate for our failure to express ourself in code. Note that I used the word failure. I meant it. Comments are always failures.” ― Robert C. Martin, Clean Code: A Handbook of Agile Software Craftsmanship
>
> “Redundant comments are just places to collect lies and misinformation.” ― Robert C. Martin, Clean Code: A Handbook of Agile Software Craftsmanship
>
> "Comments are not a substitute for good code. If the code needs a comment to be understood, it would be better to rewrite the code to make it clearer." — Steve McConnell, Code Complete


## The Setup

While reviewing a Django model recently, I stumbled on this code:

```python
@property
def first_book_edition_name(self):
    # Note: using all() instead of first() to avoid an extra database query
    books = self.books.all()
    for book in books:
        return book.edition.name
    return None
```

At first glance, this seems reasonable. It avoids `first()` and instead iterates over `.all()` to return the first result. The comment suggests that this was done to **avoid an extra database query.**

But after digging in… that comment doesn’t tell the whole story. In fact, it may be misleading.


## The Real Behavior

Let’s break it down:

- `.all()` in Django returns a **lazy queryset**.
- Iterating that queryset (e.g., in `for book in books`) causes Django to **fire a SQL query** that retrieves **all matching rows**, not just the first one.
- Even though the loop returns after the first result, the query itself has **already fetched the full result set**.

And more importantly:
- Accessing `book.edition.name` triggers a **second query**, unless the related `edition` was fetched up front.  In this case, it is not.

So this pattern:

```python
books = library.books.all()
for book in books:     
    return book.edition.name
```

Will result in **two queries**, despite what the comment implies:
1. One for the full set of `books`
2. Another for the related `edition`

## The Cleaner, More Efficient Version

Instead, we can use Django’s `select_related()` to perform a **join** and fetch both tables in a single query:

```python
# Use select_related to fetch both Book and Edition in a single query
book = library.books.select_related('edition').first()
if book:
    return book.edition.name
```

This triggers a single query like:

```sql
SELECT ... FROM testapp_book
LEFT OUTER JOIN testapp_edition ON testapp_book.edition_id = testapp_edition.id
WHERE testapp_book.library_id = 1 ORDER BY ... LIMIT 1
```

It’s faster, clearer, and doesn’t rely on fragile iteration logic just to return the first result.

## But Wait — What About Performance?

It's true that `select_related()` performs a **SQL join**, which can bring in more data up front.

So is it always better?

> In our case: **yes**, because:
> - The table is small (has few entries).
> - We're only fetching **one row**.
> - We **always** access the related `edition`.

There’s no value in deferring the lookup — it’s guaranteed to happen.

However, in larger tables or when the related field is **optional or infrequently accessed**, lazy loading (and potentially even `.only()` or `.defer()`) may be more appropriate.


## 🔍 Key Takeaways

- Don’t trust comments blindly — inspect what the code (and the ORM) actually does.
- `.first()` is not inherently inefficient. It's often more optimal than `.all()` when only one result is needed.
- `select_related()` is your friend when you know you’ll access related data immediately.
- Always profile or check query logs if performance matters.

## 🧹 Final Notes
In the end, the original comment — though well-intentioned — was both incorrect and misleading. As always, trust the queries, not the assumptions.

We’ve updated these properties in the model to use `select_related()` and `.first()`, improving both clarity and efficiency. Thanks to whoever left the comment for giving us a fun little mystery to unravel.

I have provided some sample code to illustrate this issue.  The sample code is the functional equivalent of what I discovered in production, though obivously streamlined for simplicity and re-written to protect corporate IP rights.

