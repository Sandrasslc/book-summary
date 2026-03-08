# Chapter Recognition Regex Patterns

## Chinese Patterns

```regex
# Standard chapter format
^第[一二三四五六七八九十百千零\d]+[章回节部卷]

# Matching examples:
# 第一章 开始       (Chapter 1: The Beginning)
# 第二十三章 决战   (Chapter 23: The Final Battle)
# 第1回 悟空出世    (Episode 1: The Birth of Sun Wukong)
# 第三节 方法论     (Section 3: Methodology)
```

```regex
# Simple ordinal numbers (Chinese)
^[一二三四五六七八九十]+[、\.]
```

```regex
# Arabic numerals
^\d+[\.\、]\s*.+
```

## English Patterns

```regex
^Chapter\s+\d+.*$
^Part\s+\d+.*$
^Section\s+\d+.*$
```

## Combined Pattern

Use `|` to combine multiple patterns for searching:

```
(^第[一二三四五六七八九十百千零\d]+[章回节部卷])|(^Chapter\s+\d+)|(^\d+[\.\、]\s*.+)
```

## Chapter Boundary Detection

Content between two chapter headings belongs to the preceding chapter:

```
Chapter 1          ← Chapter 1 starts (line 100)
  content...
Chapter 2          ← Chapter 2 starts (line 250)
```

- Chapter 1 range: lines 100–249
- Chapter 2 range: line 250 to the next chapter
