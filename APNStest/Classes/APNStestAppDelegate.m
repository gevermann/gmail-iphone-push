//
//  APNStestAppDelegate.m
//  APNStest
//
//  Created by Gunnar Evermann on 4/18/09.


#import "APNStestAppDelegate.h"
#import "APNStestViewController.h"

@implementation APNStestAppDelegate

@synthesize window;
@synthesize viewController;

- (void)application:(UIApplication *)application didRegisterForRemoteNotificationsWithDeviceToken:(NSData *)devToken {
	
//    const void *devTokenBytes = [devToken bytes];
	NSLog(@"device tokesn: %@", devToken);
	
//    self.registered = YES;
	
//    [self sendProviderDeviceToken:devTokenBytes]; // custom method
	
}


- (void)application:(UIApplication *)application didFailToRegisterForRemoteNotificationsWithError:(NSError *)err {
	
    NSLog(@"Error in registration. Error: %@", err);
	
}

- (void)applicationDidFinishLaunching:(UIApplication *)application {    
    
    // Override point for customization after app launch    
									    
//	[[UIApplication sharedApplication] unregisterForRemoteNotifications];
	
	
	[[UIApplication sharedApplication] registerForRemoteNotificationTypes:(UIRemoteNotificationTypeBadge | UIRemoteNotificationTypeSound | UIRemoteNotificationTypeAlert)];

	[window addSubview:viewController.view];
    [window makeKeyAndVisible];
}


- (void)dealloc {
    [viewController release];
    [window release];
    [super dealloc];
}


@end
