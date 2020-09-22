# replaCy Article Agreer

A replaCy extension to manage indirect article agreement, that is, to deal with making "a" and "an" be correct so you don't have to think about them in your matches.

## Install

`poetry add replacy_article_agreer`

## Usage

```python
import en_core_web_sm
from replacy import ReplaceMatcher
from replacy.db import load_json
from replacy_article_agreer import ArticleAgreer
from spacy.util import filter_spans


nlp = en_core_web_sm.load()
replaCy = ReplaceMatcher(nlp, load_json('path to match dict(s)'))

aa = ArticleAgreer()

# filtering spans first isn't strictly necessary, but recommended
replaCy.add_pipe(filter_spans, name="filter_spans", before="joiner")
replaCy.add_pipe(aa, name="article_agreer", after="filter_spans")
```
