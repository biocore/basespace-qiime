function launchSpec(dataProvider)
{
    var ret = {
        
        appSessionName: "bsq pre-alpha",
        commandLine: [ "bash", "/script.sh" ],
        //containerImageId: "yoshikiv/qiime-basespace-count-seqs"
        //containerImageId: "yoshikiv/debugging-count-seqs"
        containerImageId: "yoshikiv/bsq-debugging"
        // Options: [ "bsfs.enabled=true" ]
    };
    return ret;
}

// example multi-node launch spec
/*
function launchSpec(dataProvider)
{
    var ret = {
        nodes: []
    };
    
    ret.nodes.push({
        appSessionName: "Hello World 1",
        commandLine: [ "cat", "/illumina.txt" ],
        containerImageId: "basespace/demo",
        Options: [ "bsfs.enabled=true" ]
    });
    
    ret.nodes.push({
        appSessionName: "Hello World 2",
        commandLine: [ "cat", "/illumina.txt" ],
        containerImageId: "basespace/demo",
        Options: [ "bsfs.enabled=true" ]
    });
    
    return ret;
}
*/

/* 
function billingSpec(dataProvider) {
    return [
    {
        "Id" : "insert product ID here",
        "Quantity": 1.0
    }];
}
*/
