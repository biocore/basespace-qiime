function launchSpec(dataProvider)
{
    var ret = {
        // see script.sh in this folder 
        appSessionName: "bsq pre-alpha",
        commandLine: [ "bash", "/upstream.sh" ],
        containerImageId: "yoshikiv/bsq-debugging"
    };
    return ret;
}
