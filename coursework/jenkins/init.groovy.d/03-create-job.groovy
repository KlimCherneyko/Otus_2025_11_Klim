import jenkins.model.Jenkins
import hudson.triggers.TimerTrigger
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition
import org.jenkinsci.plugins.workflow.job.WorkflowJob

def instance = Jenkins.getInstance()
def jobName = "saucedemo-booker-tests"
def jenkinsfile = new File("/coursework/Jenkinsfile")

if (!jenkinsfile.exists()) {
    println("Jenkinsfile not found at /coursework/Jenkinsfile — skip job creation")
    return
}

def job = instance.getItem(jobName)
if (job == null) {
    job = instance.createProject(WorkflowJob, jobName)
    job.addTrigger(new TimerTrigger("H/30 * * * *"))
}

job.setDefinition(new CpsFlowDefinition(jenkinsfile.text, true))
job.save()
println("Updated pipeline job ${jobName} from /coursework/Jenkinsfile")
