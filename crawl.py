# This buffer is for notes you don't want to save, and for Lisp evaluation.
#;; If you want to create a file, visit that file with C-x C-f,
#;; then enter the text in that file's own buffer.

import urllib2;
import pdb;
import io;

urlPrefix = 'http://contracts.onecle.com';
contentCount = 0;

def extractList(sourceURL, regionHead, regionEnd, patternHead, patternEnd):
    #pdb.set_trace();    
    resultList = [];

    try:
        response = urllib2.urlopen(sourceURL);
    except urllib2.HTTPError as e:
        print(e.code);
    except urllib2.URLError as e:        
        print (e.reason);
    else:
        page = response.read();

        pos = 0;
        posend = 0;
        start = 0;
    
        current = "";    
        pos = page.rfind(regionHead);
        
        current = page[pos:];
    #pos = current.find(patternHead);
    #current = current[pos:];
    
        posend = current.find(regionEnd);
        current = current[ :posend];

        postemp = current.find(patternHead);
        current = current[postemp:];
        start = 0;
        end = current.find(patternEnd);

        while (start != -1):
            url = current[start:end];
            resultList.append(url);

            current = current[end+1:];
            start = current.find(patternHead);
            end = current.find(patternEnd);

    return resultList;

def extractContent(sourceURL, patternHead, patternEnd):
    #pdb.set_trace();    
    current = "";

    try:
        response = urllib2.urlopen(sourceURL);
    except urllib2.HTTPError as e:
        print("error: " + e.code);
    except urllib2.URLError as e:        
        print("error" + e.reason);
    else:
        page = response.read();

        pos = 0;
        posend = 0;
        start = 0;
        
        pos = page.rfind(patternHead);
        current = page[pos:];
        posend = current.find(patternEnd);
        current = current[ :posend];

    return current;


def crawlIndex():
    print("f: crawlIndex");
    
    sourceURL = urlPrefix + "/type";
    print("crawl: " + sourceURL);
    
    regionHead = "http://contracts.onecle.com/type/316.shtml";
    regionEnd = "</ul></td></tr></table>";

    patternHead = "http";
    patternEnd = "\">";

    linkList = extractList(sourceURL, regionHead, regionEnd, patternHead, patternEnd);
    io.writeList(linkList, io.getLinkFileNameIndex());

    patternHeadTheme = "\">";
    patternEndTheme = "</a>";
    
    themeList = extractList(sourceURL, regionHead, regionEnd, patternHeadTheme, patternEndTheme);
    themeList = [theme[2:] for theme in themeList];
    io.writeList(themeList, io.getThemeFileNameIndex());

    resultDict = {};
    for i in range(len(linkList)):
        key = themeList[i];
        value = linkList[i];
        resultDict[key] = value;
    
    return resultDict;
    
def crawlType(linkThemeDict):
    print("f: crawlType");
    
    regionHead = "<h2 class=\"index\">";
    regionEnd = "</div>";

    patternHead = "href=\"";
    patternEnd = "\">";

    patternHeadTheme = "shtml\">";
    patternEndTheme = "</a>";

    resultDict = {};
    for key in linkThemeDict:        
        print("crawl: " + key);
        print(linkThemeDict[key]);
        
        sourceURL = linkThemeDict[key];
        fileName = key;
#        if sourceURL == "http://contracts.onecle.com/type/29.shtml":
#            pdb.set_trace();
        
        linkList = extractList(sourceURL, regionHead, regionEnd, patternHead, patternEnd);
        
        themeList = extractList(sourceURL, regionHead, regionEnd, patternHeadTheme, patternEndTheme);

        linkList = [link[6:] for link in linkList];
        themeList = [theme[7:] for theme in themeList];

        io.writeList(linkList, io.getLinkFileNameWithPathInTypeDir(fileName));
        io.writeList(themeList, io.getThemeFileNameWithPathInTypeDir(fileName));

        currentDict = {};
        for i in range(len(linkList)):
            #pdb.set_trace();
            if linkList[i].find("shtml") == -1:
                continue;
            else:
                currentDict[themeList[i]] = linkList[i];
        
        resultDict[key] =currentDict;

    # for j, di in resultDict.iteritems():
    #     print(j + ":::");
    #     for k, value in di.iteritems():
    #         print(k);
    #         print(value);

    # resultStr = "";
    # for j, di in resultDict.iteritems():
    #     resultStr += j + ":::";
    #     for k, value in di.iteritems():
    #         resultStr += k + "###" + value;            
    return resultDict;        

def crawlContent(typeName, themeList, linkList):
    print("f: crawlContent");

    io.mkdirInContent(typeName);
    resultList = [];
    for i in range(len(themeList)):
        print("crawl: " + themeList[i]);
        global contentCount;
        contentCount += 1;
        
        theme = themeList[i];
        url = urlPrefix + linkList[i];
        print(url);
        
        regionHead = "<pre>";
        regionEnd = "<h4>";

        patternHead = "<pre>";
        patternEnd = "</pre>";
        #pdb.set_trace();
        #contentList = [];
        #contentList = extract(url, patternHead, patternEnd);
        content = "";
        content = extractContent(url, patternHead, patternEnd);
        content = content[5:];
#        print content;

        fileName = theme;
        # if fileName == "Concession Contract - Border's Parking SRL and MercadoLibre SA":
        #     pdb.set_trace();

        #     print theme;
        #     print url;
        io.writeContent(content, io.getFileNameWithPathInContentDir(typeName, fileName));
        resultList.append(content);
    return resultList;

def test():

    global contentCount;
    contentCount += 1;    
    
    
        
def main():
    # test();
#    pdb.set_trace();
    
    io.mkdirDataRepo();
#    indexDict = crawlIndex();
#    typeDict = crawlType(indexDict);

    
    typeDict = io.readType(io.readIndex());
    #sigle thread version, for each type in type index, crawl the content
    for key, di in typeDict.iteritems():
        themeList = di.keys();
        linkList = di.values();
        
        crawlContent(key, themeList, linkList);
    return;

if __name__ == "__main__":
    main();
