iisnode encountered an error when processing the request.

```
HRESULT: 0x6d
HTTP status: 500
HTTP subStatus: 1013
HTTP reason: Internal Server Error
```

You are receiving this HTTP 200 response because [system.webServer/iisnode/@devErrorsEnabled](https://github.com/tjanczuk/iisnode/blob/master/src/samples/configuration/web.config) configuration setting is 'true'.
In addition to the log of stdout and stderr of the node.exe process, consider using [debugging](http://tomasz.janczuk.org/2011/11/debug-nodejs-applications-on-windows.html) and [ETW traces](http://tomasz.janczuk.org/2011/09/using-event-tracing-for-windows-to.html) to further diagnose the problem.
The node.exe process has not written any information to stderr or iisnode was unable to capture this information. Frequent reason is that the iisnode module is unable to create a log file to capture stdout and stderr output from node.exe. Please check that the identity of the IIS application pool running the node.js application has read and write access permissions to the directory on the server where the node.js application is located. Alternatively you can disable logging by setting [system.webServer/iisnode/@loggingEnabled](https://github.com/tjanczuk/iisnode/blob/master/src/samples/configuration/web.config) element of web.config to 'false'.
