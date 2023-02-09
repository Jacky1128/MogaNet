_base_ = [
    '../../_base_/models/fpn_moganet.py',
    '../../_base_/datasets/ade20k.py',
    '../../_base_/default_runtime.py'
]

# model settings
model = dict(
    type='EncoderDecoder',
    backbone=dict(
        type='MogaNet_feat',
        arch='large',
        drop_path_rate=0.3,
        frozen_stages=1,
        init_cfg=dict(
            type='Pretrained', 
            checkpoint=\
                'https://github.com/Westlake-AI/MogaNet/releases/download/moganet-in1k-weights/moganet_large_sz224_8xbs64_ep300.pth.tar',
            ),
        ),
    neck=dict(in_channels=[64, 160, 320, 640]),
    decode_head=dict(num_classes=150))

gpu_multiples = 2  # we use 8 gpu instead of 4 in mmsegmentation, so lr*2 and max_iters/2
# optimizer
optimizer = dict(type='AdamW', lr=0.0001 * gpu_multiples, weight_decay=0.0001)
optimizer_config = dict()
# learning policy
lr_config = dict(policy='poly', power=0.9, min_lr=0.0, by_epoch=False)
# runtime settings
runner = dict(type='IterBasedRunner', max_iters=160000 // gpu_multiples)
checkpoint_config = dict(by_epoch=False, interval=8000 // gpu_multiples, max_keep_ckpts=1)
evaluation = dict(interval=8000 // gpu_multiples, metric='mIoU', save_best='auto')
