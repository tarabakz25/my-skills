---
theme: seriph
background: https://cover.sli.dev
title: Presentation Title
info: |
  ## Presentation Description
  Brief description of your presentation.

  By Your Name
class: text-center
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
---

# Presentation Title

Subtitle or Tagline

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Press Space to continue <carbon:arrow-right class="inline"/>
  </span>
</div>

<div class="abs-br m-6 flex gap-2">
  <button @click="$slidev.nav.openInEditor()" title="Open in Editor" class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon:edit />
  </button>
  <a href="https://github.com/slidevjs/slidev" target="_blank" alt="GitHub" title="Open in GitHub"
    class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon-logo-github />
  </a>
</div>

<!--
Presenter notes go here.
You can write anything you want to remember.
-->

---
transition: fade-out
---

# What is This About?

Brief introduction to your topic

- Point 1
- Point 2
- Point 3

<br>
<br>

Read more about [Why this matters](https://example.com)

<!--
Here are some notes for the presenter
-->

---
layout: default
---

# Table of Contents

<Toc minDepth="1" maxDepth="2"></Toc>

---
layout: section
---

# Section 1

## Getting Started

---

# Slide with Two Columns

Use two-column layout to present information side-by-side

::left::

## Left Side

- Point A
- Point B
- Point C

::right::

## Right Side

- Point X
- Point Y
- Point Z

---
layout: image-right
image: https://cover.sli.dev
---

# Image on Right

Content with an image on the right side.

- Bullet point 1
- Bullet point 2
- Bullet point 3

---
layout: center
class: text-center
---

# Centered Content

This slide has centered content both horizontally and vertically.

<div class="pt-8">
  <button @click="$slidev.nav.next" class="px-4 py-2 rounded border border-current">
    Continue
  </button>
</div>

---
layout: quote
---

# "An inspiring quote that relates to your topic"
— Author Name

---
layout: fact
---

# 100%
Amazing Statistic

---
layout: section
---

# Section 2

## Main Content

---

# Lists and Animations

Click animations make content appear step by step

<v-clicks>

- First item appears
- Then second item
- Then third item
- Finally fourth item

</v-clicks>

<div v-click class="mt-8 text-xl">
  All done!
</div>

---

# Conclusion

Summary of main points

<v-clicks>

1. Key takeaway #1
2. Key takeaway #2
3. Key takeaway #3

</v-clicks>

<div v-click class="mt-12 text-center">

## Thank You!

Questions?

</div>

---
layout: end
---

# Thank You

Contact: your.email@example.com

<div class="abs-br m-6">
  <a href="https://github.com/yourusername" target="_blank" class="text-xl slidev-icon-btn opacity-50">
    <carbon-logo-github />
  </a>
  <a href="https://twitter.com/yourusername" target="_blank" class="text-xl slidev-icon-btn opacity-50">
    <carbon-logo-twitter />
  </a>
</div>
