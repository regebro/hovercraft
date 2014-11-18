<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns="http://www.w3.org/1999/xhtml">

<xsl:import href="resource:templates/reST.xsl" />

<xsl:template match="step" name="slide">
    <section>
      <xsl:copy-of select="@*"/>
      <xsl:apply-templates />
    </section>
</xsl:template>

<xsl:template match="/" name="main">
<html>
  <head>
    <title><xsl:value-of select="/document/@title"/></title>
    <meta name="generator" content="Hovercraft! 1.0 http://regebro.github.com/hovercraft"/>
    <xsl:if test="/document/author"> <!-- Author is a child to the document, everything else become attributes -->
      <meta name="author">
        <xsl:attribute name="content">
          <xsl:value-of select="/document/author" />
        </xsl:attribute>
      </meta>
    </xsl:if>
    <xsl:if test="/document/@description">
      <meta name="description">
        <xsl:attribute name="content">
          <xsl:value-of select="/document/@description" />
        </xsl:attribute>
      </meta>
    </xsl:if>
    <xsl:if test="/document/@keywords">
      <meta name="keywords">
        <xsl:attribute name="content">
          <xsl:value-of select="/document/@keywords" />
        </xsl:attribute>
      </meta>
    </xsl:if>

  <xsl:for-each select="/document/templateinfo/header/css">
    <link rel="stylesheet">
      <xsl:copy-of select="@*"/>
    </link>
  </xsl:for-each>

  <xsl:for-each select="/document/templateinfo/header/js">
    <script type="text/javascript">
      <xsl:copy-of select="@*"/>
    </script>
  </xsl:for-each>

  </head>
  <body class="impress-not-supported">

  <xsl:for-each select="/document">
    <div class="reveal">
      <!-- Any section element inside of this container is displayed as a slide -->
        <div class="slides">
            <xsl:apply-templates />
        </div>
    </div>
  </xsl:for-each>

  <xsl:for-each select="/document/templateinfo/body/js">
    <script type="text/javascript">
      <xsl:copy-of select="@*"/>
    </script>
  </xsl:for-each>

  <script>

  // Full list of configuration options available here:
  // https://github.com/hakimel/reveal.js#configuration
  Reveal.initialize({
    controls: true,
    progress: true,
    history: true,
    center: true,

    theme: Reveal.getQueryHash().theme, // available themes are in /css/theme
    transition: Reveal.getQueryHash().transition || 'default', // default/cube/page/concave/zoom/linear/fade/none

    // Parallax scrolling
    // parallaxBackgroundImage: 'https://s3.amazonaws.com/hakim-static/reveal-js/reveal-parallax-1.jpg',
    // parallaxBackgroundSize: '2100px 900px',

    // Optional libraries used to extend on reveal.js
    dependencies: [
    // None yet.
  ]
});

  </script>

</body>
</html>
</xsl:template>

</xsl:stylesheet>
