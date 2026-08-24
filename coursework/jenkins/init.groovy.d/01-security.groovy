import jenkins.model.Jenkins
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import hudson.security.HudsonPrivateSecurityRealm

def instance = Jenkins.getInstance()
def realm = new HudsonPrivateSecurityRealm(false)

if (realm.getAllUsers().isEmpty()) {
    realm.createAccount("admin", "admin")
    instance.setSecurityRealm(realm)

    def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
    strategy.setAllowAnonymousRead(false)
    instance.setAuthorizationStrategy(strategy)
    instance.save()
}
