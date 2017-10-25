
.. vim: si:et:ts=4:sw=4:tw=120

.. This is an rST document. See Python Docutils for more details on the format and how to process it:
.. http://docutils.sourceforge.net/

.. Text width is 120 characters with hard wraps, set your terminal / editor accordingly.


:Title:         Documentation tools proposal
:Author:        jf.lefillatre
:Version:       0.8
:Date:          2016/03/11


.. TODO: add tables to summarize the differences between formats
.. TODO: add chapters for diagrams and picture formats


Goals
=====

The goal of this document is to establish a baseline for the tools and formats used for documentation of ClusterVision 
technical projects. Currently it only targets the Trinity development project, but the choices made should be sane 
enough to be reused for other purposes in development and engineering.



Documentation production process
================================

The documentation writing process can be roughly split in the following steps:

#. Content writing

   Various authors (developers, engineers, etc) write the body of the documentation. At that point it doesn't have to
   be anything more than a collection of notes, sorted by topic (software, task, etc). It may also include pictures and
   diagrams to illustrate the notes. Those notes do not include additional formatting yet.

#. Editing

   The notes are merged together, structured and organized following a table of contents. The quality of the writing is
   checked, abbreviations are removed and the various writing styles are homogenized. References to external content
   (pictures, links) are checked.
   The ToC itself may have been predefined, or it may be created on the fly based on the available content.

#. Checking

   The grammar and spelling of the document are checked and any mistake is corrected. The tools used for this are
   referred to as *checkers* or *checking tools*.

#. Formatting

   Additional metadata is added to the document to direct the final appearance of the documentation. The syntax of
   those additions is referred to as the *source format*, and the documents formatted with the source format are
   referred to as the *source documentation*.

#. Output document creation

   The source documentation is processed by a *document processor* or *document converter* to convert from the source
   format to the *output format*. Accordingly, the resulting documentation is referred to as *output documentation*.


Outside of output document creation, most of the steps will be in fact mixed up and the process will be an incremental
loop rather than a strict step-by-step procedure. But in the end, every bit of documentation will have passed through
each of those steps at least once.

As this document is not about writing or editing, it will address exclusively the three last items, or:

- what is the best source format;
- what output formats are required;
- what document processor to use;
- what are the best checking tools.



General requirements
====================

When gathering feedback and comments from engineers, we reached a consensus on the following technical requirements:

- the source format must permit easy collaboration;
- it must be possible to generate multiple output formats from the same sources;
- it must be possible to keep track of changes in a VCS;
- searching across multiple files (especially source files) must be straightforward;
- source formatting must be simple enough to not interfere with reading or writing additional content;
- the source format must have native UTF-8 support and all documentation should be UTF-8-clean;
- the source format must not be tied to a specific software tool or a specific platform.

I would also add the following items:

- the documentation format should support a system of templates, in order to maintain a consistent corporate identity
  across all output formats;
- it must be easy to check for spelling and grammar mistakes in the source files;
- it must be possible to include pictures in the output documents.

An extra implicit requirement is that those tools and formats must be well supported under Linux and other members of
the UNIX tree (Apple OS X), as those are the platforms that most devs and engineers use for their work.



Source format
=============

From the beginning, the `General requirements`_ eliminate various possibilities as being incompatible with one or more
mandatory items:

**Binary formats**:
    Such formats include Microsoft Word's DOC and OpenOffice/LibreOffice's ODT. It is easier to list what requirements
    they match, rather than the ones they don't: UTF-8, templates support and, for MS Office, checking tools. None of
    those formats were designed for technical documentation.

**Online-based tools and formats**:
    Also known as: Google Docs. It is designed for real-time collaborative editing, but there is no source format
    available outside of Google Docs, and the only output formats available are PDF and Microsoft binary formats.
    It doesn't work very well for structured documents, and encourages the fragmentation of content into a lot of short
    documents with the directory layout as a basic structure.

**HTML, XML or SGML-based formats**:
    Designed for computer processing, they are to various extents unreadable and unwritable by humans. Some tools use
    XML or SGML as an intermediate format, which isn't a problem as long as we're not expected to edit it. The best
    known XML-based format for technical documentation is DocBook_, but `Wikipedia's List of XML markup languages`_
    contains many others for every imaginable purpose.

**Postscript, [tg]roff or TeX-based formats**:
    Although very powerful and widely used, those tools were first and foremost designed for typesetting. Their syntaxes
    are rich and complex but hard to master and not really adapted to collaborative editing (it's just too easy to ruin
    the layout or break macros!). Like XML, tools that use TeX or LaTeX as an intermediate format are accepted as long
    as no interaction is required.

**Obscure or platform-specific formats**:
    The description says it all: niche, unsupported or restrictive formats are useless for our purpose. Those include
    Microsoft RTF, and online services custom markup languages as used by some Wiki or BBS platforms.


What comes out of that process of elimination is that we need a mainstream, documentation-oriented, text-based source
format with lightweight formatting. There are multiple such lightweight markup languages listed on `Wikipedia's
Lightweight markup language page`_, some quite well-known and others more confidential. I will only focus on the three
better known, used and maintained formats in that list: **AsciiDoc**, **Markdown** and **reStructuredText**.

To start with, all three formats match all requirements for our source format. They have many similarities in their
respective designs and they all the same basic functionalities, which are enough for basic documentation tasks. Their
syntaxes are different enough that some writers may prefer one over the other, but there is no major technical advantage
of one over the others. The final choice will depend heavily on tool availability and support, and other non-core
differences.

There are many discussions online about the vices and virtues of all three languages, and comparisons of various
syntaxes. Those are usually incomplete; one such example is available here_. Most discussions usually end up in a draw
and the personal preferences seem to be the overriding deciding factors.

AsciiDoc_ is basically a human friendly version of DocBook. It is semantically equivalent to DocBook, and therefore can
be used to create any documentation that can be done in DocBook. It is supported by the AsciiDoc tools, as well as an
alternative implementation called Asciidoctor_. Both convert AsciiDoc to HTML and DocBook, and from DocBook many other
formats can be generated. Wikipedia says that it's used by GitHub and some major documentation projects. It's a mature,
stable project, and it seems to be the most professional of the three (which is not surprising given its DocBook roots).
It has the richest and most powerful syntax, a full specification and lots of documentation.

Markdown_ may be the most famous of the lightweight markup languages, and its name is often used as a generic
description for any of those languages. It has the widest support of all languages, both as libraries or modules to read
or write it and as plugins for popular editors. It is used mostly for web page generation and wiki purposes; GitHub and
Reddit use it for example.  Because it was never standardized properly, numerous slightly incompatible extensions and
dialects of the language exist, and those aren't supported very well. Pandoc (see `Document converters`_) lists 5
different supported variants: ``markdown``, ``markdown_github``, ``markdown_mmd``, ``markdown_phpextra`` and
``markdown_strict``. Documentation quality varies from one dialect to another.

reStructuredText_ (or RST, or rST, or reST, or whatever you can think of) was created originally as the documentation
standard for the Python project, but evolved into a general-purpose language. The umbrella project for the tools and the
language itself is called Docutils_. Like AsciiDoc, it has been adopted by various projects for their documentation, and
is supported by Trac, GitHub and BitBucket. Like AsciiDoc again, it has a proper specification and a good amount of
documentation.


.. _Docbook: http://www.docbook.org/
.. _Wikipedia's List of XML markup languages: https://en.wikipedia.org/wiki/List_of_XML_markup_languages
.. _Wikipedia's Lightweight markup language page: https://en.wikipedia.org/wiki/Lightweight_markup_language
.. _here: http://hyperpolyglot.org/lightweight-markup
.. _AsciiDoc: http://asciidoc.org/
.. _Asciidoctor: http://asciidoctor.org/
.. _Markdown: http://daringfireball.net/projects/markdown/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Docutils: http://docutils.sourceforge.net/



Output formats
==============

So far, the required output formats are:

- PDF, for customer distribution;
- HTML, for online documentation (both internal and external);
- man pages, for delivery with the software.

It may be useful to be able to generate specific formats for wikis too, although not necessary as many wiki engines now
support standard markup syntaxes. Therefore, having the possibility of converting a given source format to one supported
by a wiki is a bonus but not a requirement.

All three lightweight markdown languages are supported by tools that allow generation of all required output formats,
either directly or through an intermediate format (PDF goes through DocBook or LaTeX). In the latter case, most tools
come with scripts that hide the intermediate conversion and produce the output directly.

Although it is not a requirement, it may be possible to create presentations (slides) with some input formats. It
may require writing some custom LaTeX + Beamer code, so for that specific usage Google Docs may be simply better.

.. TODO: do we want to support mobile formats like EPUB? They are supported by most tools anyway, so it wouldn't add any
.. complexity really.



Available tools
===============

Document converters
-------------------

All three source formats come with their respective tools to convert formatted text into HTML and other formats. As
mentioned earlier, they may do a two-step conversion through an intermediate format, but it's mostly invisible to the
user. The exceptions to the rule are some Markdown extensions, which were designed especially for website-only
use and have very poor support outside of their platform. Also, none of the native tools allow conversion from one
markup language to another, only from their language to end-user formats.

Some generic documentation converters also exist, the best known and most complete of which is certainly Pandoc_. Not
only can it convert from one markup language to the other, it can also replace entirely the native tools and be used
exclusively as a global document converter. The formats it supports are numerous; the one installed on my system
displays those lists::

    pandoc 1.15.1.1
    Input formats:  commonmark, docbook, docx, epub, haddock, html, json*, latex,
                    markdown, markdown_github, markdown_mmd, markdown_phpextra,
                    markdown_strict, mediawiki, native, odt, opml, org, rst, t2t,
                    textile, twiki
                    [ *only Pandoc's JSON version of native AST]
    Output formats: asciidoc, beamer, commonmark, context, docbook, docx, dokuwiki,
                    dzslides, epub, epub3, fb2, haddock, html, html5, icml, json*,
                    latex, man, markdown, markdown_github, markdown_mmd,
                    markdown_phpextra, markdown_strict, mediawiki, native, odt,
                    opendocument, opml, org, pdf**, plain, revealjs, rst, rtf, s5,
                    slideous, slidy, texinfo, textile
                    [**for pdf output, use latex or beamer and -o FILENAME.pdf]


One notable exception is that it doesn't accept AsciiDoc as an input format, but it can convert both Markdown and
reStructuredText to AsciiDoc or directly to DocBook. Also, just like native tools it emits LaTeX as an intermediate
format on the way to PDF.

Pandoc is also the only tool of which I know that can deal with so many dialects of Markdown. It does so by accepting a
very loose syntax: all dialects (including Pandoc's own) are merged into the default ``markdown`` format, even including
bits of rST syntax when it's better than Markdown's, and it tries to make sense of what it parses. It is possible to
limit the syntax to one specific dialect on the command line, but I don't know how compliant those outputs are given the
lack of documentation. Still, Pandoc is the best tool for Markdown and a very convenient all-in-one converter.



Spelling and grammar
--------------------

Linux has been known for a long time for its lack of good spelling and grammar checkers. Many spellcheckers are
available (``ispell``, ``aspell``, ``hunspell`` and ``enchant``, which is a common interface for all the ``*spell``),
but they have different dictionary formats, different features and the quality varies a lot. Usually no grammar
checking is available at all. This is one area where Microsoft Word keeps a huge lead over the UNIX world.

Outside of those spell checkers, I could find trace of only one project fit for this purpose: LanguageTool_. It is
written in Java, can run as an OpenOffice/LibreOffice plugin, standalone with an interactive GUI, standalone as a pure
checker or as a server. It supports both spell and grammar checking of many languages, although the quality of each
varies depending on the language.

The interactive GUI is a major strong point as it displays its recommendations and offers either automatic changes or
manual modification of the contents. Conversely, it has no notion of the syntax of the source document nor of the fact
that there may be code examples mixed in. It will try to parse and correct the code, which would be wrong of course.
That fact alone makes impossible automatic batch correction of documents.


.. _Pandoc: http://pandoc.org/
.. _LanguageTool: https://www.languagetool.org/



Recommended choices
===================

Regarding the **source format**, making a choice is not easy. I have used Markdown to write official documentation in
other jobs, and I am writing this document in reStructuredText. The only format that I haven't used extensively yet is
AsciiDoc, but after studying all three formats for a week or so, I believe that it is the best one.

The fragmentation of Markdown is a real issue. When writing in Markdown, I ended up using Pandoc-specific features and
including a header in my files warning readers that Pandoc would be required to process it. This defect makes Markdown
the least desirable of all three languages.

Between reStructuredText and AsciiDoc, I believe that the latter one offers more possibilities for professional
publishing than rST. It includes some typesetting commands that can make it a little less readable than rST, but which
offer more control over the appearance of tables and other non-text elements (think of it as a little taste of LaTeX, in
a way). I don't think that there is anything wrong with rST, but in the end AsciiDoc seems to be slightly better adapted
to the goal of publishing technical documentation in multiple formats.

In favor of rST, due to its Python roots it enjoys better support by online services. Converting from AsciiDoc to rST is
cumbersome as it involves going through DocBook, and the procedure won't be supported by services that pull directly
from the GitHub repository.

I would like to recommend AsciiDoc as a standard input format for the documentation. But it is likely that our
documentation releases will be purely online and may rely on third-party web services, and the lack of support for
AsciiDoc would be an issue. For that reason, I recommend that the documentation be written in reStructuredText. It is
supported natively by GitHub and many other web services, has good tool support and can be converted to other formats
with Pandoc if needed.

As for the **spell and grammar checker**, there is no real recommendation to make -- there is only one choice. It is not
perfect but I don't know of anything better. I have been using it as an OpenOffice plugin for years, and although it
doesn't catch everything it helps a lot. One has to keep in mind its limitations, and the last careful check will always
have to be done by a human editor.

