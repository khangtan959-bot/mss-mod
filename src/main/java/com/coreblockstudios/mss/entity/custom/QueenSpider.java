package com.coreblockstudios.mss.entity.custom;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.animal.IronGolem;
import net.minecraft.world.entity.animal.SnowGolem;
import net.minecraft.world.entity.monster.CaveSpider;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.monster.Spider;
import net.minecraft.world.entity.npc.AbstractVillager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

public class QueenSpider extends Monster {
    private int summonCooldown = 0;
    private int rangedModeTimer = 0;
    private boolean isRangedMode = false;

    public QueenSpider(EntityType<? extends Monster> type, Level level) {
        super(type, level);
        this.xpReward = 300;
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 150.0D)
                .add(Attributes.ATTACK_DAMAGE, 12.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.3D)
                .add(Attributes.FOLLOW_RANGE, 24.0D)
                .add(Attributes.ARMOR, 4.0D)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.8D)
                .add(Attributes.SCALE, 2.0D);
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(1, new FloatGoal(this));
        this.goalSelector.addGoal(3, new MeleeAttackGoal(this, 1.0D, true));
        this.goalSelector.addGoal(7, new RandomStrollGoal(this, 1.0D));
        this.goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 6.0F));
        this.goalSelector.addGoal(9, new RandomLookAroundGoal(this));

        this.targetSelector.addGoal(1, new HurtByTargetGoal(this));
        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
        this.targetSelector.addGoal(3, new NearestAttackableTargetGoal<>(this, AbstractVillager.class, false));
    }

    @Override
    public void tick() {
        super.tick();
        if (!this.level().isClientSide() && this.tickCount % 20 == 0) {
            updateCombatMode();
        }
    }

    private void updateCombatMode() {
        if (this.getTarget() == null) return;

        double dist = this.distanceToSqr(this.getTarget());
        if (dist > 64.0D && !isRangedMode) {
            switchToRanged();
        } else if (dist <= 49.0D && isRangedMode) {
            switchToMelee();
        }

        if (summonCooldown > 0) summonCooldown--;
        if (isRangedMode) {
            rangedModeTimer--;
            if (rangedModeTimer <= 0) {
                switchToMelee();
            }
        }
    }

    private void switchToRanged() {
        isRangedMode = true;
        rangedModeTimer = 80;
    }

    private void switchToMelee() {
        isRangedMode = false;
        rangedModeTimer = 0;
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hurt = super.doHurtTarget(target);
        if (hurt && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.POISON, 60, 2), this);

            if (summonCooldown <= 0 && this.level() instanceof ServerLevel serverLevel) {
                summonMinions(serverLevel);
                summonCooldown = 200;
            }
        }
        return hurt;
    }

    private void summonMinions(ServerLevel level) {
        for (int i = 0; i < 4; i++) {
            Spider spider = new Spider(EntityType.SPIDER, level);
            summonEntityNearby(spider, level);
        }
        if (this.random.nextFloat() < 0.3F) {
            CaveSpider caveSpider = new CaveSpider(EntityType.CAVE_SPIDER, level);
            summonEntityNearby(caveSpider, level);
        }
    }

    private void summonEntityNearby(LivingEntity entity, ServerLevel level) {
        double x = this.getX() + (this.random.nextDouble() - 0.5) * 6.0;
        double z = this.getZ() + (this.random.nextDouble() - 0.5) * 6.0;
        double y = this.getY();
        BlockPos pos = BlockPos.containing(x, y, z);
        while (!level.getBlockState(pos).isAir() && pos.getY() < this.getY() + 3) {
            pos = pos.above();
        }
        entity.setPos(pos.getX() + 0.5, pos.getY(), pos.getZ() + 0.5);
        level.addFreshEntity(entity);
    }
}
