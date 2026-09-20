from vscode.base.business_objects import ObjectFactory


class ConfigurablePropertiesManager():
    @staticmethod
    def getConfigurableProps():
        if not VSPersistableSystemOption.configurableProps:
            props = ObjectFactory().getConfigurableProperties()
            if props:
                VSPersistableSystemOption.configurableProps = {} 
                for cp in props:
                    VSPersistableSystemOption.configurableProps[cp.getPropertyName()] = cp
                         