<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="3.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei">

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>

   
    <xsl:template match="/">
        <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <title><xsl:value-of select="//tei:title[1]"/></title>
                <style>
                    body {
                        font-family: 'Courier New', monospace;
                        background: rgba(0, 0, 0, 0.94);
                        padding: 40px;
                        display: flex;
                        justify-content: center;
                    }

                    .letter-container {
                        height: 800px;
                        width: 641px;
                        padding: 40px;
                        background: rgb(173, 167, 127);
                        box-shadow: 0 0 10px rgba(0,0,0,0.1);
                        position: relative;
                    }

                    .orgName {
                        text-align: center;
                        font-size: 1.5em;
                        font-weight: bold;
                        margin-bottom: 1em;
                    }

                    .date {
                        text-align: right;
                    }

                    .address {
                        text-align: center;
                    }

                    .vertical-text {
                        writing-mode: vertical-rl;
                        text-orientation: upright;
                        white-space: nowrap;
                        font-size: 1.2em;
                        font-weight: bold;
                        margin-right: 5px;
                        letter-spacing: 3px;
                        position: absolute;
                        top: 120px;
                    }

                    .letter-body {
                        margin-top: 6em;
                    }
                    .letter-body .salute {
                         display: block;
                         margin-left: 7em;      /* 2.5em + 4.5em */
                         text-indent: -4.5em;  /* 抵消段落缩进 */
                        line-height: 1.5;
                    }
                    .letter-body p {
                        text-indent: 4.5em;  
                        line-height: 1.5;
                        margin-left: 2.5em;
                    }
          
                    .signature {
                        margin-top: 3em;
                        padding-top: 1em;
                        text-align: center;
                    }

                    .postscript {
                        margin-top: 2em;
                    }

                    .handwritten {
                        font-family: cursive;
                        color: #444;
                        font-size: 1em;
                        text-align: center;
                    }
                </style>
            </head>
            <body>
                <div class="letter-container">
                    <div class="letterhead">
                        <div class="orgName">
                            <xsl:value-of select="//tei:orgName"/>
                        </div>
                        <div class="date">
                            <xsl:value-of select="//tei:dateline/tei:date"/>
                        </div>
                        <div class="address">
                            <xsl:apply-templates select="//tei:dateline/tei:address"/>
                        </div>
                        <div class="vertical-text">
                             <xsl:value-of select="//tei:opener/tei:address/tei:addrLine"/>
                        </div>
                    </div>
                   
                    <div class="letter-body">
                         <div class="salute">
                          <xsl:apply-templates select="//tei:opener/tei:salute"/>
                         </div>
                         <div>
                            <xsl:apply-templates select="//tei:div[@type='body']"/>
                         </div>
                    </div>

                    
                    <div class="signature">
                        <xsl:apply-templates select="//tei:closer"/>
                    </div>

                   
                    <div class="postscript">
                        <xsl:apply-templates select="//tei:postscript"/>
                    </div>
                </div> 
            </body>
        </html>
    </xsl:template>

    
    <xsl:template match="tei:div[@type='body']">
        <p style="text-indent: 5em;">
            <xsl:apply-templates/>
        </p>
    </xsl:template>

   
    <xsl:template match="tei:lb">
        <br/>
    </xsl:template>


   
    <xsl:template match="tei:del[@rend='overstrike']">
        <span style="text-decoration: line-through; color: #666;">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    
    <xsl:template match="tei:persName">
        <xsl:value-of select="."/>
    </xsl:template>

    
    <xsl:template match="tei:address">
        <div class="address">
            <xsl:apply-templates select="tei:persName"/>
            <xsl:apply-templates select="tei:addrLine"/>
            <xsl:apply-templates select="tei:settlement"/>
        </div>
    </xsl:template>

   
    <xsl:template match="tei:addrLine">
        <p><xsl:value-of select="."/></p>
    </xsl:template>

    
    <xsl:template match="tei:settlement">
        <p><xsl:value-of select="."/></p>
    </xsl:template>

    
    <xsl:template match="tei:closer">
        <p style="text-align: right;">
            <xsl:apply-templates/>
        </p>
    </xsl:template>

   
    <xsl:template match="tei:postscript/tei:p">
        <p class="handwritten">
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    
    <xsl:template match="tei:add">
        <span class="handwritten">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    
    <xsl:template match="text()[contains(., 'write to')]">
        <xsl:value-of select="substring-before(., 'write')"/>
        <span style="font-size: small; vertical-align: super;">one</span>
        <xsl:text> write to </xsl:text>
        <xsl:value-of select="substring-after(., 'write to')"/>
    </xsl:template>

</xsl:stylesheet>
