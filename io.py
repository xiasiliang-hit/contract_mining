#indexfile = 'index.txt';
import os;


dataDir = "./data/";
typeDir = dataDir + "type/";
contentDir = dataDir + "content/";

linkSuffix = ".link";
themeSuffix = ".theme";
contentSuffix = ".txt";
indexFileBase = "index";

logFile = "log.txt";

def writeList(contentList, fileName):
    print "wrtieList: " + fileName;
        
    contentList = [item + '\n' for item in contentList];
    output = open(fileName, 'w');
    output.writelines(contentList);
    output.close();
    return;

def writeContent(content, fileName):
    print "writeContent: " + fileName;
        
    if len(fileName) >= 255:
        fileName = fileName[:255-1];
        
    output = open(fileName, 'w');
    output.write(content);
    output.close();
    return;

def readList(fileName):
    print "readList: " + fileName;
    
    inFile = open(fileName, 'r');
    itemList = inFile.readlines();
    inFile.close();

    itemList = [item[:-1] for item in itemList];
    return itemList;



def readIndex():
    print "readIndex: ";
    
    fileName = getThemeFileNameIndex();
    resultList = readList(fileName);
    return resultList;

def readType(themeList):
    print "readType: ";
    #pdb.set_trace();

    resultDict = {};
    for theme in themeList:
        fileTheme = getThemeFileNameWithPathInTypeDir(theme);
        typeList = readList(fileTheme);
        #inFile = open(fileTheme, 'r');
        #typeList = inFile.readlines();
        
        fileLink = getLinkFileNameWithPathInTypeDir(theme);
        linkList = readList(fileLink);
        #inFile = open(fileLink, 'r');
        #linkList = inFile.readlines();
        tempDict = {};
        for i in range(len(typeList)):
            aType = typeList[i];
            aLink = linkList[i];
            
            tempDict[aType] = aLink;
            resultDict[theme] = tempDict;
    return resultDict;


def getLinkFileNameIndex():
    return dataDir + indexFileBase + linkSuffix;
def getThemeFileNameIndex():
    return dataDir + indexFileBase + themeSuffix;

def getLinkFileNameWithPathInTypeDir(fileName):
    return typeDir + fileName.replace('/', ' ') + linkSuffix;
def getThemeFileNameWithPathInTypeDir(fileName):
    return typeDir + fileName.replace('/', ' ') + themeSuffix;

def getFileNameWithPathInContentDir(typeName, fileName):
    return contentDir + typeName + '/' + fileName.replace('/', ' ') + contentSuffix;
#def getThemeFileNameWithPathInContentDir(fileName):
#    return contentDir + fileName.replace('/', ' ') + themeSuffix;
    
def mkdirInContent(typeName):
    directory = contentDir + typeName;
    if not os.path.exists(directory):
        os.makedirs(directory);
    return;

def mkdirDataRepo(): 
    if not os.path.exists(dataDir):
        os.makedirs(dataDir);
        print("mkdir: " + dataDir);
        
    if not os.path.exists(typeDir):
        os.makedirs(typeDir);
        print("mkdir: " + typeDir);
        
    if not os.path.exists(contentDir):
        os.makedirs(contentDir);
        print("mkdir: " + contentDir);
        
    return;
        
def writeLog():
    output = open(dataDir + logFile + logSuffix, "w+");
    output.writeLines(logList);
    output.close();

def test():
    print(getLinkFileNameWithPathInTypeDir("a/b/c"));

def main():
    test();
    return;

if __name__ == "__main__":
    main();
