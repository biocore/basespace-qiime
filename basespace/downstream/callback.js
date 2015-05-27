function launchSpec(dataProvider)
{
    var ret = {
        // see script.sh in this folder 
        appSessionName: "basespace-qiime pre-alpha",
        commandLine: [ "bash", "/downstream.sh" ],
        containerImageId: "yoshikiv/basespace-qiime-191"
    };
    return ret;
}

