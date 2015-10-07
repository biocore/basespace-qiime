function launchSpec(dataProvider)
{
    var ret = {
        // see script.sh in this folder 
        appSessionName: "basespace-qiime pre-alpha",
        commandLine: [ "bash", "/downstream.sh" ],
        containerImageId: "yoshikiv/basespace-qiime-191-dev@sha256:470b4ae8960a28309fdeabe06caea6728cfe6d70cbce7c7e3c5d2dd017927cc6",
        Options: [ "bsfs.enabled=true" ]
    };
    return ret;
}