<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:import href="resource:templates/reST.xsl" />

<xsl:template match="/" name="main">
<html>
  <head>
    <title><xsl:value-of select="/document/@title"/></title>
  </head>
  <body class="impress-not-supported">
  
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
