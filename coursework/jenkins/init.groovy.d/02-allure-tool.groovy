import jenkins.model.Jenkins
import org.allurereport.jenkins.tools.AllureCommandlineInstallation

try {
    def instance = Jenkins.getInstance()
    def descriptor = instance.getDescriptorByType(AllureCommandlineInstallation.DescriptorImpl.class)
    def installation = new AllureCommandlineInstallation("Allure", "/opt/allure", [])
    descriptor.setInstallations(installation)
    descriptor.save()
    println("Registered Allure commandline at /opt/allure")
} catch (Exception exception) {
    println("Failed to register Allure commandline: ${exception}")
}
