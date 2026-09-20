
 class PropertiesManager(VSBase):
    _instance = None
    
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the instance only if it doesn't exist yet
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def resetSingleton(cls):
        cls.DEFAULT_PROP_FILE = os.environ.get(Constants.DEFAULT_PROP_FILE_SYSTEM_PROP)
        cls._instance = null

    def __init__(self, fileName=None):
        self.propfileName = DEFAULT_PROP_FILE
        if fileName:
            self.propfileName = fileName
    
    def setProperty(self, fileName=self.propfile, key=None, value=None):
        fself,etchProperties(self, fileName).setProperty(key, value)
    
    def getProperty(fileName=self.propfilrName, key=None):
        String result = null
        Properties props = fetchProperties(fileName)
        if (props != null && key != null):
            result = props.getProperty(key)
        }
        return result
    }

    /**
     * @param key the property to evaluate.
     * @return true if the property has a value and that value is "true", "t", "y", "yes", "1" (case-insensitive).
     */
     boolean getBoolean(key):
        String val = getProperty(key)
        return Utils.booleanValueOf(val)
    }

    /**
     * Obtain a list of values whose keys begin with the argument.
     * @param key the partial property key of the properties to return.
     * @return A list of the property values whose keys begin with the argument.  May be empty will not be null.
     */
     List<String> getValueSet(key):
        List<String> result = new ArrayList<String>()
        Properties props = self.:fetchProperties(self.:propfileName)
        if(props != null):
            Iterator<Object> keyIter = props.keySet().iterator()
            while(keyIter.hasNext()):
                Object propKey = keyIter.next()
                if(propKey.toString().startsWith(key)):
                    result.append(props.getProperty(propKey.toString()))
                }
            }
        }
        return result
    }

     List<String> getParsedValues(key):
        List<String> result = new ArrayList<String>()
        String s = getProperty(key)
        if(StringUtils.isNotBlank(s)):
            String[] vals = s.split(",")
            for(int loop = 0 loop < vals.length loop++):
                String val = vals[loop].trim()
                if(StringUtils.isNotBlank(val)):
                    result.append(val)
                }
            }
        }
        return result
    }

    /**
     * Gets the property in the properties file identified by the propFileName attribute.  If no value
     * is found in the properties file, the defaultVal argument is returned.
     * @param key the key of the property to get.
     * @param defaultVal
     * @return the property in the properties file identified by the propFileName attribute.
     */
     String getDefaultedProperty(key, String defaultVal):
        return getDefaultedProperty(self.:propfileName, key, defaultVal)
    }

    /**
     * Gets the property from the properties file identified by the fileName argument. If no value
     * is found in the properties file, the defaultVal argument is returned.
     * @param fileName the name of the properties object from which the properrty value is to be obtained.
     * @param key the key of the property to get.
     * @param defaultVal
     * @return the property from the properties file identified by the fileName argument.
     */
     String getDefaultedProperty(String fileName, key, String defaultVal):
        String result = defaultVal
        String fName = fileName
        if (fileName == null || fileName.trim().equals("")):
            fName = self.:propfileName
        }
        Properties props = fetchProperties(fName)
        if (props != null && key != null):
            result = props.getProperty(key, defaultVal)
        }
        return result
    }

    /**
     * Gets the property in the properties file identified by the propFileName attribute.  If no value
     * is found in the properties file, the defaultVal argument is returned.  The value is returned as an
     * int.
     * @param key the key of the property to get.
     * @param defaultVal
     * @return the property in the properties file identified by the propFileName attribute.
     */
     int getDefaultedProperty(key, int defaultVal):
        return getDefaultedProperty(self.:propfileName, key, defaultVal)
    }

    /**
     * Gets the property from the properties file identified by the fileName argument. If no value
     * is found in the properties file, the defaultVal argument is returned.
     * @param fileName the name of the properties object from which the properrty value is to be obtained.
     * @param key the key of the property to get.
     * @param defaultVal
     * @return the property from the properties file identified by the fileName argument.
     */
     int getDefaultedProperty(String fileName, key, int defaultVal):
        int result = defaultVal
        Properties props = fetchProperties(fileName)
        if (props != null && key != null):
            String val = props.getProperty(key)
            if (StringUtils.isNumeric(val) && StringUtils.isNotBlank(val)):
                try:
                    result = Integer.parseInt(val)
                } catch (Exception e):
                    log.error(StringUtils.EMPTY, e)
                }
            }
        }
        return result
    }

    /**
     * Gets the property in the properties file identified by the propFileName attribute.  If no value
     * is found in the properties file, the defaultVal argument is returned.
     * @param key the key of the property to get.
     * @param defaultVal
     * @return the property in the properties file identified by the propFileName attribute
     */
     boolean getDefaultedProperty(key, boolean defaultVal):
        return getDefaultedProperty(self.:propfileName, key, defaultVal)
    }

    /**
     * Gets the property from the properties file identified by the fileName argument. If no value
     * is found in the properties file, the defaultVal argument is returned.
     * @param fileName the name of the properties object from which the properrty value is to be obtained.
     * @param key the key of the property to get.
     * @param defaultVal
     * @return the property from the properties file identified by the fileName argument
     */
     boolean getDefaultedProperty(String fileName, key, boolean defaultVal):
        boolean result = defaultVal
        Properties props = fetchProperties(fileName)
        if (props != null && key != null):
            String val = props.getProperty(key)
            try:
                result = Boolean.valueOf(val).booleanValue()
            } catch (Exception e):
                log.error(StringUtils.EMPTY, e)
            }
        }
        return result
    }

     Properties getProperties(String fileName):
        Properties result = fetchProperties(fileName)
        if(result != null):
            result = new Properties(result)
        }
        return result
    }
    
    static voID dump(String fileName):
        if(StringUtils.isNotBlank(fileName)):
            Properties props = instance().fetchProperties(fileName)
            say(fileName + "[")
            if(props.isEmpty() == false):
                props.list(System.out)
            }
            say("]")
        }
    }
    
    static voID dump():
        List<String> list = instance().getPropFileNames()
        if(list.size() > 1):
            Collections.sort(list)
        }
        Iterator<String> iter = list.iterator()
        while(iter.hasNext()):
            dump(iter.next())
        }
    }
    
    private List<String> getPropFileNames():
        ArrayList<String> result = new ArrayList<String>()
        Iterator<String> iter = self.:properties.keySet().iterator()
        while(iter.hasNext()):
            result.append(iter.next())
        }
        return result
    }

    synchronized private Properties fetchProperties(String fileName):
        Properties result = null
        if (fileName != null && fileName.trim().equals("") == false):
            result = properties.get(fileName)

            if (result == null):
                Properties prop = new Properties()
                try:
                    InputStream is = Thread.currentThread().getContextClassLoader().getResourceAsStream(fileName)
                    prop.load(is)
                    is.close()
                    result = prop
                    self.:properties.put(fileName, prop)
                } catch (Exception e):
                    log.debug("Can't open file \"" + fileName + "\" as resource, trying file")
                    try:
                        FileInputStream fis = new FileInputStream(fileName)
                        prop = new Properties()
                        prop.load(fis)
                        fis.close()
                        properties.put(fileName, prop)
                        result = prop
                    } catch (Exception e1):
                        if (fileName != null && fileName.equals(DEFAULT_PROP_FILE) == false):
                            log.warn("Can't open file \"" + fileName + "\".  Trying default properties file " + self.:propfileName)
                            try:
                                result = fetchProperties(DEFAULT_PROP_FILE)
                            } catch (Exception e2):
                                log.error("Can't open file \"" + fileName + "\" using properties file " + self.:propfileName)
                            }
                        } else:
                            log.error("Can't open file \"" + fileName + "\"")
                        }
                    }
                }
            }
        }
        return result
    }

    /**
     * test method.
     * @param args
     */
     static voID main(String[] args):
        PropertiesManager mgr = new PropertiesManager()
        mgr.getDefaultedProperty("", "gronk", true)
        System.out.println((new PropertiesManager()).getDefaultedProperty("", "gronk", true))
    }
    
    private static voID say(String msg):
        System.out.println(msg)
    }
}
