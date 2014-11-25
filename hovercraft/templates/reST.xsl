<!--
	 Copyright (c) 2006, Michael Alyn Miller <malyn@strangeGizmo.com>.
	 All rights reserved.

	 Redistribution and use in source and binary forms, with or without
	 modification, are permitted provided that the following conditions
	 are met:

	 1.  Redistributions of source code must retain the above copyright
		 notice unmodified, this list of conditions, and the following
		 disclaimer.
	 2.  Redistributions in binary form must reproduce the above
		 copyright notice, this list of conditions and the following
		 disclaimer in the documentation and/or other materials provided
		 with the distribution.
	 3.  Neither the name of Michael Alyn Miller nor the names of the
		 contributors to this software may be used to endorse or promote
		 products derived from this software without specific prior
		 written permission.

	 THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS "AS IS"
	 AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
	 TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
	 PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR
	 CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
	 SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
	 LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
	 USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
	 ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
	 OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
	 OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
	 SUCH DAMAGE.
-->

<!-- Modifications by Lennart Regebro, 2013:

* Added support for the <notes>-tag.

* Changed literal block rendering from a <div class="literal-block"> to <pre>,
  with @classes copied over to @class for syntax highlighting.

* Added support for the <inline> tag for code highlighting.

Modification by Carl Mayer, 2013:

* Skipped rendering of ReST comments.

-->

<xsl:stylesheet
	version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="http://www.w3.org/1999/xhtml">



<!-- Suppress the reST document title, information, and topic name.
	 These values should be pulled in by the main XSL template. -->
<xsl:template match="/document/title" />
<xsl:template match="/document/docinfo" />
<xsl:template match="/document/topic" />

<!-- Suppress all field lists.  These are only used for 'special
	 features' implemented by the author of the site-specific reST
	 content. -->
<xsl:template match="field_list" />



<!-- ===================================================================
	 Inline elements.
 -->

<xsl:template match="emphasis">
	<em><xsl:apply-templates /></em>
</xsl:template>

<xsl:template match="literal">
	<tt><xsl:apply-templates /></tt>
</xsl:template>

<xsl:template match="reference">
	<xsl:element name="a">
		<xsl:attribute name="href">
			<xsl:choose>
				<xsl:when test="@refid">
					<xsl:value-of select="concat('#', @refid)" />
				</xsl:when>
				<xsl:when test="@refuri">
					<xsl:value-of select="@refuri" />
				</xsl:when>
			</xsl:choose>
		</xsl:attribute>

		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<xsl:template match="strong">
	<strong><xsl:apply-templates /></strong>
</xsl:template>



<!-- ===================================================================
	 Body elements.
 -->


<!-- Generic body elements. -->
<xsl:template match="image">
	<xsl:element name="img">
		<xsl:attribute name="src">
			<xsl:value-of select="@uri" />
		</xsl:attribute>
		<xsl:if test="@alt">
			<xsl:attribute name="alt">
				<xsl:value-of select="@alt" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@width">
			<xsl:attribute name="width">
				<xsl:value-of select="@width" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@height">
			<xsl:attribute name="height">
				<xsl:value-of select="@height" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@classes">
			<xsl:attribute name="class">
				<xsl:value-of select="@classes" />
			</xsl:attribute>
		</xsl:if>
	</xsl:element>
</xsl:template>


<xsl:template match="line_block">
	<div class="line-block">
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="line_block/line">
    <xsl:apply-templates /><br />
</xsl:template>


<xsl:template match="literal_block">
	<pre class="highlight">
		<xsl:attribute name="class">
			<xsl:value-of select="concat('highlight ', @classes)" />
		</xsl:attribute>
		<xsl:apply-templates />
	</pre>
</xsl:template>

<xsl:template match="literal_block/br">
	<br />
</xsl:template>


<xsl:template match="paragraph">
	<p>
        <xsl:if test="@classes">
	<xsl:attribute name="class">
		<xsl:value-of select="@classes" />
	</xsl:attribute>
        </xsl:if>
	<xsl:apply-templates />
        </p>
</xsl:template>

<xsl:template match="container">
	<div>
        <xsl:if test="@classes">
	<xsl:attribute name="class">
		<xsl:value-of select="@classes" />
	</xsl:attribute>
        </xsl:if>
        <xsl:if test="@ids">
	<xsl:attribute name="id">
		<xsl:value-of select="@ids" />
	</xsl:attribute>
        </xsl:if>
	<xsl:apply-templates />
        </div>
</xsl:template>

<xsl:template match="substitution_definition" />



<!-- reST block quotes get prepended with a paragraph that reads
	 "ATTRIBUTION wrote:" where ATTRIBUTION is the contents of the
	 reStructuredText attribution (the information after the
	 double-hyphens). -->
<xsl:template match="block_quote">
	<blockquote>
		<xsl:apply-templates/>
	</blockquote>

	<xsl:if test="./attribution">
		<div class="cite">
			<span class="cite_label">Source: </span>
			<cite><xsl:apply-templates select="attribution/*|attribution/text()" /></cite>
		</div>
	</xsl:if>
</xsl:template>

<!-- Suppress block_quote/attribution elements since we grab the text of
	 the attribution from the block_quote template. -->
<xsl:template match="block_quote/attribution" />


<!-- Footnote references are wrapped in brackets ([..]) and enclosed in
	 an anchor tag with the class "footnoteref". -->
<xsl:template match="footnote_reference">
    <xsl:element name="a">
        <xsl:attribute name="class">footnoteref</xsl:attribute>
        <xsl:attribute name="id">
            <xsl:text>footnote-backref-</xsl:text>
            <xsl:value-of select="@ids" />
        </xsl:attribute>
        <xsl:attribute name="href">
            <xsl:text>#footnote-</xsl:text>
            <xsl:value-of select="@refid" />
        </xsl:attribute>

        <xsl:text>[</xsl:text>
        <xsl:apply-templates />
        <xsl:text>]</xsl:text>
    </xsl:element>
</xsl:template>

<!-- The footnote itself is wrapped in a div tag with a class of
	 "footnote".  The footnote begins with an anchor tag (class name
	 "footnotereturn") that links back to the part of the document where
	 the footnote appeared. -->
<xsl:template match="footnote">
    <xsl:element name="div">
        <xsl:attribute name="class">footnote</xsl:attribute>
        <xsl:attribute name="id">
            <xsl:text>footnote-</xsl:text>
            <xsl:value-of select="@ids" />
        </xsl:attribute>

		<xsl:element name="a">
			<xsl:attribute name="class">footnotereturn</xsl:attribute>
			<xsl:attribute name="href">
				<xsl:text>#footnote-backref-</xsl:text>
				<xsl:value-of select="@backrefs" />
			</xsl:attribute>
			<xsl:attribute name="title">
				<xsl:text>return to content</xsl:text>
			</xsl:attribute>

			<xsl:text>#</xsl:text>
			<xsl:value-of select="label" />
			<xsl:text>: </xsl:text>
		</xsl:element>

        <xsl:apply-templates />
    </xsl:element>
</xsl:template>
<xsl:template match="footnote/label" />


<!-- Basic lists. -->
<xsl:template match="bullet_list">
	<ul><xsl:apply-templates /></ul>
</xsl:template>

<xsl:template match="enumerated_list">
	<ol><xsl:apply-templates /></ol>
</xsl:template>

<!-- Basic list items. -->
<xsl:template match="list_item">
	<li><xsl:apply-templates /></li>
</xsl:template>

<!-- TODO Lists are currently stripped of their paragraph wrapping.
	This may or may not be what you want.  You could use a match value
	of "list_item/paragraph[count(child::*) = 0]" to detect simple vs.
	complex paragraphs, although this would also catch inline elements.
	A stunningly-complex match value should probably be created to
	detect the list type (simple or complex) and then put all of the
	items into the same wrapper (either a p tag or a bare list item). -->
<xsl:template match="list_item/paragraph">
<xsl:apply-templates />
</xsl:template>


<!-- Definition lists. -->
<xsl:template match="definition_list">
	<dl><xsl:apply-templates /></dl>
</xsl:template>

<xsl:template match="definition_list_item/term">
	<dt><xsl:apply-templates /></dt>
</xsl:template>

<xsl:template match="definition_list_item/definition">
	<dd><xsl:apply-templates /></dd>
</xsl:template>


<!-- Option lists. -->
<xsl:template match="option_list">
	<table class="option-list" cellpadding="0" cellspacing="0">
		<tr>
			<th>Option</th>
			<th>Description</th>
		</tr>

		<xsl:apply-templates />
	</table>
</xsl:template>

<xsl:template match="option_list_item">
	<tr><xsl:apply-templates /></tr>
</xsl:template>

<xsl:template match="option_group">
	<td>
		<xsl:for-each select="option">
			<xsl:apply-templates select="." /><br />
		</xsl:for-each>
	</td>
</xsl:template>

<xsl:template match="option_group/option">
	<span class="option-string"><xsl:value-of select="option_string" /></span>
	<xsl:if test="option_argument">
		<span class="option-delimiter"><xsl:value-of select="option_argument/@delimiter" /></span>
		<span class="option-argument"><xsl:value-of select="option_argument" /></span>
	</xsl:if>
</xsl:template>

<xsl:template match="option_list_item/description">
	<td><xsl:apply-templates /></td>
</xsl:template>


<!-- Raw HTML elements are passed straight through.  Note that this
	 assumes that the output document is an XHTML document. -->
<xsl:template match="raw[@format='html']">
	<xsl:value-of select="." disable-output-escaping="yes" />
</xsl:template>


<!-- Section titles are wrapped in a heading tag.  The heading level
	 (h1, h2, h3, etc.) is set by counting the number of parent sections
	 that this section is enclosed in. -->
<xsl:template match="section/title">
	<xsl:element name="{concat('h', format-number(count(ancestor::section), '#'))}">
		<xsl:attribute name="id">
			<xsl:value-of select="parent::section/@ids" />
		</xsl:attribute>

		<xsl:apply-templates />
	</xsl:element>
</xsl:template>


<!-- Tables.

	 These are pretty much handled as you would expect.  The only custom
	 feature is a pair of special fields that can be used to control the
	 horizontal and vertical alignment of the table cells.

	 If you want to set a custom horizontal alignment, include the field
	 ":table-cell-halign:" directly before the table.  Each of the cells
	 (td elements) will include an "align" attribute with the specified
	 value.

	 A similar field exists for specifying the valign value.  This field
	 is called ":table-cell-valign:".  -->
<xsl:template match="table">
	<table cellpadding="0" cellspacing="0">
        <xsl:if test="@classes">
	<xsl:attribute name="class">
		<xsl:value-of select="@classes" />
	</xsl:attribute>
        </xsl:if>
        <xsl:if test="@ids">
	<xsl:attribute name="id">
		<xsl:value-of select="@ids" />
	</xsl:attribute>
        </xsl:if>
	<xsl:apply-templates />
	</table>
</xsl:template>

<xsl:template match="thead">
	<thead><xsl:apply-templates /></thead>
</xsl:template>

<xsl:template match="thead/row">
	<tr><xsl:apply-templates /></tr>
</xsl:template>

<xsl:template match="thead/row/entry">
	<xsl:element name="th">
		<xsl:if test="@morecols">
			<xsl:attribute name="colspan">
				<xsl:value-of select="format-number(1 + @morecols, '#')" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@morerows">
			<xsl:attribute name="rowspan">
				<xsl:value-of select="format-number(1 + @morerows, '#')" />
			</xsl:attribute>
		</xsl:if>

		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<xsl:template match="tbody">
	<tbody><xsl:apply-templates /></tbody>
</xsl:template>

<xsl:template match="tbody/row">
	<tr><xsl:apply-templates /></tr>
</xsl:template>

<xsl:template match="tbody/row/entry">
	<xsl:element name="td">
		<xsl:if test="@morecols">
			<xsl:attribute name="colspan">
				<xsl:value-of select="format-number(1 + @morecols, '#')" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@morerows">
			<xsl:attribute name="rowspan">
				<xsl:value-of select="format-number(1 + @morerows, '#')" />
			</xsl:attribute>
		</xsl:if>
        <xsl:if test="ancestor::table/preceding-sibling::*[1]/field/field_name[text()='table-cell-halign']">
			<xsl:attribute name="align">
                <xsl:value-of select="ancestor::table/preceding-sibling::*[1]/field/field_name[text()='table-cell-halign']/../field_body/paragraph" />
			</xsl:attribute>
        </xsl:if>
        <xsl:if test="ancestor::table/preceding-sibling::*[1]/field/field_name[text()='table-cell-valign']">
			<xsl:attribute name="valign">
                <xsl:value-of select="ancestor::table/preceding-sibling::*[1]/field/field_name[text()='table-cell-valign']/../field_body/paragraph" />
			</xsl:attribute>
        </xsl:if>

		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<xsl:template match="inline">
	<span>
		<xsl:attribute name="class">
			<xsl:value-of select="@classes" />
		</xsl:attribute>
		<xsl:apply-templates />
	</span>
</xsl:template>

<!-- Skip ReST comments -->
<xsl:template match="comment">
</xsl:template>

</xsl:stylesheet>
