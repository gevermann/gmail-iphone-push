//
//  APNStestAppDelegate.h
//  APNStest
//
//  Created by Gunnar Evermann on 4/18/09.


#import <UIKit/UIKit.h>
#import <UIKit/UIApplication.h>

@class APNStestViewController;

@interface APNStestAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
    APNStestViewController *viewController;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet APNStestViewController *viewController;

@end

