<xsl:stylesheet
	version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="http://www.w3.org/1999/xhtml">

<xsl:template match="image">
        <xsl:element name="img">
                <xsl:attribute name="src">
                        <xsl:value-of select="@uri" />
                </xsl:attribute>
                <xsl:if test="@description">
                        <xsl:attribute name="alt">
                                <xsl:value-of select="@description" />
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
		<xsl:if test="@style">
			<xsl:attribute name="style">
				<xsl:value-of select="@style" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@crossorigin">
			<xsl:attribute name="crossorigin">
				<xsl:value-of select="@crossorigin" />
			</xsl:attribute>
		</xsl:if>
        </xsl:element>
</xsl:template>

<xsl:template match="video">
	<xsl:element name="video">
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
		<xsl:if test="@id">
			<xsl:attribute name="id">
				<xsl:value-of select="@id" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@style">
			<xsl:attribute name="style">
				<xsl:value-of select="@style" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@crossorigin">
			<xsl:attribute name="crossorigin">
				<xsl:value-of select="@crossorigin" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@autoplay">
			<xsl:attribute name="data-Media-autoplay" />
		</xsl:if>
		<xsl:if test="@controls">
			<xsl:attribute name="controls" />
		</xsl:if>
		<xsl:if test="@muted">
			<xsl:attribute name="muted" />
		</xsl:if>
		<xsl:if test="@loop">
			<xsl:attribute name="loop" />
		</xsl:if>
		<xsl:if test="@preload">
			<xsl:attribute name="preload" />
		</xsl:if>
		<xsl:if test="@poster">
			<xsl:attribute name="poster">
				<xsl:value-of select="@poster" />
			</xsl:attribute>
		</xsl:if>
		<xsl:apply-templates select="*" />
		<xsl:if test="@description">
			<xsl:value-of select="@description" />
		</xsl:if>
	</xsl:element>
</xsl:template>

<xsl:template match="audio">
	<xsl:element name="audio">
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
		<xsl:if test="@id">
			<xsl:attribute name="id">
				<xsl:value-of select="@id" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@style">
			<xsl:attribute name="style">
				<xsl:value-of select="@style" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@crossorigin">
			<xsl:attribute name="crossorigin">
				<xsl:value-of select="@crossorigin" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@autoplay">
			<xsl:attribute name="data-Media-autoplay" />
		</xsl:if>
		<xsl:if test="@controls">
			<xsl:attribute name="controls" />
		</xsl:if>
		<xsl:if test="@muted">
			<xsl:attribute name="muted" />
		</xsl:if>
		<xsl:if test="@loop">
			<xsl:attribute name="loop" />
		</xsl:if>
		<xsl:if test="@preload">
			<xsl:attribute name="preload" />
		</xsl:if>
		<xsl:apply-templates select="*" />
		<xsl:if test="@description">
			<xsl:value-of select="@description" />
		</xsl:if>
	</xsl:element>
</xsl:template>

<xsl:template match="source" name="source">
	<xsl:element name="source">
		<xsl:if test="@src">
			<xsl:attribute name="src">
				<xsl:value-of select="@src" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@mime">
			<xsl:attribute name="type">
				<xsl:value-of select="@mime" />
			</xsl:attribute>
		</xsl:if>
	</xsl:element>
</xsl:template>

<xsl:template match="track" name="track">
	<xsl:element name="track">
		<xsl:if test="@default">
			<xsl:attribute name="default" />
		</xsl:if>
		<xsl:if test="@kind">
			<xsl:attribute name="kind">
				<xsl:value-of select="@kind" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@label">
			<xsl:attribute name="label">
				<xsl:value-of select="@label" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@src">
			<xsl:attribute name="src">
				<xsl:value-of select="@src" />
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="@language">
			<xsl:attribute name="srclang">
				<xsl:value-of select="@language" />
			</xsl:attribute>
		</xsl:if>
	</xsl:element>
</xsl:template>
</xsl:stylesheet>
