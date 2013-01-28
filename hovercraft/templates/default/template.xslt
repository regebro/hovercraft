<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:import href="resource:templates/reST.xsl" />

<xsl:template match="/" name="main">
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=1024" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta http-equiv="X-UA-Compatible" content="chrome=1" />

    <title><xsl:value-of select="/document/@title"/></title>

    <link rel="stylesheet" media="print" href="css/screen.css"/>
    <link rel="stylesheet" media="screen, projection" href="css/impressConsole.css"/>
    <script type="text/javascript" src="js/impress.js"></script>
    <script type="text/javascript" src="js/impressConsole.js"></script>

  </head>
  <body class="impress-not-supported">

  <div class="fallback-message">
    <p>Your browser <b>doesn't support the features required</b> by impress.js, so you are presented with a simplified version of this presentation.</p>
    <p>For the best experience please use the latest <b>Chrome</b>, <b>Safari</b> or <b>Firefox</b> browser.</p>
  </div>

  <xsl:for-each select="/document">
    <div id="impress" transition-duration="{@transition-duration}">
      <xsl:for-each select="step">
        <div class="step">
          <xsl:copy-of select="@*"/>
          <xsl:for-each select="section">
            <xsl:apply-templates />
          </xsl:for-each>
        </div>
      </xsl:for-each>
    </div> 
  </xsl:for-each>
  
  <script src="js/impress.js"></script>
  <script src="js/impressConsole.js"></script>
  <script src="js/hovercraft.js"></script>
  
</body>
</html>
</xsl:template>

</xsl:stylesheet>
