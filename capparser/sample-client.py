import capparser
import element
import enums

alert = element.Alert(sender="FireTec", 
                        status=enums.Status.Actual,
                        msgType=enums.MsgType.Alert,
                        scope=enums.Scope.Private)
alert.setSource("FireTec")
alert.addAddress("Radio Renascença")

info = element.Info(category=[enums.Category.Fire],
                      event="Incendio Florestal em Sever do Vouga",
                      urgency=enums.Urgency.Immediate,
                      severity=enums.Severity.Severe,
                      certainty=enums.Certainty.Observed)
info.setSenderName("FireTec")
info.setInstruction("Foi detetado um possível incêndio florestal na sua área, precaução é aconselhada.")

param1 = element.Parameter(parameterName="PS", parameterValue="PS=Radio Renascença")
param2 = element.Parameter(parameterName="PI", parameterValue="PI=80XX")
param3 = element.Parameter(parameterName="AF", parameterValue="AF=95.0")
param4 = element.Parameter(parameterName="AF", parameterValue="AF=100.0")
param5 = element.Parameter(parameterName="AF", parameterValue="AF=105.0")

info.addParameter(param1)
info.addParameter(param2)
info.addParameter(param3)
info.addParameter(param4)
info.addParameter(param5)

alert.addInfo(info)

capparser.deparse(alert)