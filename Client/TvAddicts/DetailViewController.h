//
//  DetailViewController.h
//  TvAddicts
//
//  Created by Sergey Klimov on 3/18/12.
//  Copyright (c) 2012 Self-Employed. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface DetailViewController : UIViewController <UISplitViewControllerDelegate>

@property (strong, nonatomic) id detailItem;

@property (strong, nonatomic) IBOutlet UILabel *detailDescriptionLabel;

@end
