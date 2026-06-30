package com.coreblockstudios.mss.entity.custom;

import com.coreblockstudios.mss.entity.MSSEntities;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.projectile.ThrowableProjectile;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.EntityHitResult;
import net.neoforged.neoforge.event.EventHooks;

public class SpiderWebProjectile extends ThrowableProjectile {
    public SpiderWebProjectile(EntityType<? extends ThrowableProjectile> type, Level level) {
        super(type, level);
    }

    public SpiderWebProjectile(Level level, LivingEntity shooter) {
        super(MSSEntities.SPIDER_WEB.get(), shooter, level);
    }

    @Override
    protected void defineSynchedData() {
    }

    @Override
    protected void onHitEntity(EntityHitResult result) {
        super.onHitEntity(result);
        if (result.getEntity() instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 140, 2));
            living.hurt(this.damageSources().mobProjectile(this, this.getOwner() != null ? this.getOwner() : this),
                    4.0F);
        }
        this.discard();
    }

    @Override
    protected void onHitBlock(BlockHitResult result) {
        super.onHitBlock(result);
        this.discard();
    }
}
